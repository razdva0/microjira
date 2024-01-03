from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import F


class WorkSpace(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=4, default="", primary_key=True)
    last_ticket_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Table(models.Model):
    name = models.CharField(max_length=255)
    work_space = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="tables")
    number = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("number",)


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    ticket_id = models.CharField(max_length=12)
    text = models.TextField(default="")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="tickets")
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=3)
    story_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.ticket_id
