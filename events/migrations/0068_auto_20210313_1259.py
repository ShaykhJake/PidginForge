# Generated by Django 3.0.3 on 2021-03-13 12:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0067_auto_20210313_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('975be437-bf99-4852-b86e-f4303941cb9c'), max_length=260),
        ),
    ]