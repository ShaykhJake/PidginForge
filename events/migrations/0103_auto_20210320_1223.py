# Generated by Django 3.0.3 on 2021-03-20 12:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0102_auto_20210319_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('e21f62a9-fbe2-4438-a570-d87c5bc42321'), max_length=260),
        ),
    ]
