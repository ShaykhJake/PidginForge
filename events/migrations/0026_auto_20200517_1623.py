# Generated by Django 3.0.3 on 2020-05-17 16:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_auto_20200517_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('f5eb426c-ca36-482f-aa75-85d9ba47c31f'), max_length=260),
        ),
    ]
