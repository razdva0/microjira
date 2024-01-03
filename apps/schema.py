import graphene

from apps.workspaces.schema import work_space_schema


class Query(work_space_schema.Query, graphene.ObjectType):
    pass


class Mutation(work_space_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
