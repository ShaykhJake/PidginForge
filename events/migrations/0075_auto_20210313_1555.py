# Generated by Django 3.0.3 on 2021-03-13 15:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0074_auto_20210313_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('1094a760-91de-40c0-b18a-4b4335633d0c'), max_length=260),
        ),
    ]
