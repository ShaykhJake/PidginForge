# Generated by Django 3.0.3 on 2021-03-13 16:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0075_auto_20210313_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('083d345f-8050-47e3-9f0c-eeb845a8090b'), max_length=260),
        ),
    ]