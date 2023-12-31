# Generated by Django 5.0 on 2023-12-11 22:45

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('-number',),
            },
        ),
        migrations.CreateModel(
            name='WorkSpace',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(default='', max_length=4, primary_key=True, serialize=False)),
                ('last_ticket_number', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ticket_id', models.CharField(max_length=12)),
                ('text', models.TextField(default='')),
                ('level', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('story_points', models.PositiveIntegerField(default=0)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='workspaces.table')),
            ],
        ),
        migrations.AddField(
            model_name='table',
            name='work_space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='workspaces.workspace'),
        ),
    ]
