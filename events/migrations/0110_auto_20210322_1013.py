# Generated by Django 3.0.3 on 2021-03-22 10:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0109_auto_20210322_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('ee2a7e80-e25b-4896-9e23-4eb7a0642c14'), max_length=260),
        ),
    ]