import graphene
from django.db import transaction
from django.db.models import F, Q
from graphene_django import DjangoObjectType

from apps.workspaces.models import WorkSpace, Table, Ticket


class WorkSpaceType(DjangoObjectType):
    class Meta:
        model = WorkSpace


class TableType(DjangoObjectType):
    class Meta:
        model = Table


class TicketType(DjangoObjectType):
    class Meta:
        model = Ticket


class Query(graphene.ObjectType):
    workspaces = graphene.List(WorkSpaceType)
    workspace = graphene.Field(WorkSpaceType, short_name=graphene.String())
    tables = graphene.List(TableType)
    tickets = graphene.List(TicketType)

    def resolve_workspace(self, info, **kwargs):
        id = kwargs.get('id')

        if id is None:
            return
        return WorkSpace.objects.get(id=id)

    def resolve_workspaces(self, info, **kwargs):
        return WorkSpace.objects.all()

    def resolve_tables(self, info, **kwargs):
        return Table.objects.all()

    def resolve_tickets(self, info, **kwargs):
        return Ticket.objects.all()


class CreateWorkSpaceInput(graphene.InputObjectType):
    name = graphene.String()
    short_name = graphene.String()


class CreateTableInput(graphene.InputObjectType):
    name = graphene.String()
    work_space = CreateWorkSpaceInput
    number = graphene.Int()


class UpdateTableInput(CreateTableInput):
    id = graphene.Int()


class CreateTicketInput(graphene.InputObjectType):
    name = graphene.String()
    text = graphene.String()
    level = graphene.Int(required=False, default_value=3)
    story_points = graphene.Int(required=False, default_value=0)
    work_space = graphene.String()


class UpdateTicketInput(graphene.InputObjectType):
    id = graphene.Int()
    table = graphene.Int()
    name = graphene.String()
    text = graphene.String()
    level = graphene.Int(required=False, default_value=3)
    story_points = graphene.Int(required=False, default_value=0)


class CreateWorkSpace(graphene.Mutation):
    class Arguments:
        input = CreateWorkSpaceInput(required=True)

    ok = graphene.Boolean()
    work_space = graphene.Field(WorkSpaceType)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, input):
        ok = True
        work_space = WorkSpace.objects.create(name=input.name, short_name=input.short_name)
        table_names = ("todo", "in_progress", "done")
        create_tables = []
        for index, table_name in enumerate(table_names):
            create_tables.append(Table(name=table_name, work_space=work_space, number=index))
        Table.objects.bulk_create(create_tables)
        return CreateWorkSpace(ok=ok, work_space=work_space)


class CreateTable(graphene.Mutation):
    class Arguments:
        input = CreateTableInput(required=False)

    ok = graphene.Boolean()
    table = graphene.Field(TableType)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, input):
        ok = True
        Table.objects.filter(number__gte=input.number).update(number=F("number") + 1)
        table = Table.objects.create(name=input.name, work_space_id=input.work_space, number=input.number)
        return CreateTable(ok=ok, table=table)


class UpdateTable(graphene.Mutation):
    class Arguments:
        input = UpdateTableInput(required=True)

    ok = graphene.Boolean()
    table = graphene.Field(TableType)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, input):
        ok = True
        table = Table.objects.select_related("work_space").get(id=input.id)
        if table.number < input.number:
            query_filter = Q(number__gt=table.number) & Q(number__lte=input.number)
            updated_field = F("number") - 1
        else:
            query_filter = Q(number__lt=table.number) & Q(number__gte=input.number)
            updated_field = F("number") + 1
        Table.objects.filter(query_filter).update(number=updated_field)
        table.name = input.name
        table.number = input.number
        table.save()
        return UpdateTable(ok=ok, table=table)


class CreateTicket(graphene.Mutation):
    class Arguments:
        input = CreateTicketInput(required=True)

    ok = graphene.Boolean()
    ticket = graphene.Field(TicketType)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, input):
        work_space = WorkSpace.objects.prefetch_related("tables").get(short_name=input.work_space)
        work_space.last_ticket_number += 1
        work_space.save()
        ok = True
        ticket = Ticket.objects.create(
            name=input.name,
            ticket_id=work_space.short_name + "-" + str(work_space.last_ticket_number),
            text=input.text,
            table=work_space.tables.get(number=0),
            level=input.level,
            story_points=input.story_points,
        )
        return CreateTicket(ok=ok, ticket=ticket)


class UpdateTicket(graphene.Mutation):
    class Arguments:
        input = UpdateTicketInput(required=True)

    ok = graphene.Boolean()
    ticket = graphene.Field(TicketType)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, input):
        ok = True
        ticket = Ticket.objects.select_related("table__work_space").get(id=input.id)
        ticket.name = input.name
        ticket.text = input.text
        ticket.table_id = input.table
        ticket.level = input.level
        ticket.story_points = input.story_points
        ticket.save()
        return UpdateTicket(ok=ok, ticket=ticket)


class Mutation(graphene.ObjectType):
    create_work_space = CreateWorkSpace.Field()
    create_table = CreateTable.Field()
    update_table = UpdateTable.Field()
    create_ticket = CreateTicket.Field()


work_space_schema = graphene.Schema(query=Query, mutation=Mutation)
