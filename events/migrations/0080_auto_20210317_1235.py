# Generated by Django 3.0.3 on 2021-03-17 12:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0079_auto_20210317_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('ebe2eb6a-b16d-46cb-b837-06fbd69aeaec'), max_length=260),
        ),
    ]