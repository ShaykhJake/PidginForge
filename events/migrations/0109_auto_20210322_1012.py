# Generated by Django 3.0.3 on 2021-03-22 10:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0108_auto_20210320_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('951465d9-86a7-40d9-9976-ebcfa06e9fb4'), max_length=260),
        ),
    ]