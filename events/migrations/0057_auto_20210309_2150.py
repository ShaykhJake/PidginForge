# Generated by Django 3.0.3 on 2021-03-09 21:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0056_auto_20210220_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('932d439f-1af9-4e78-b1f7-86721f316183'), max_length=260),
        ),
    ]
