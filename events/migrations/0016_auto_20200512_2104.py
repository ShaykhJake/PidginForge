# Generated by Django 3.0.3 on 2020-05-12 21:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20200512_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('09fa522f-1bec-4d58-9488-60fc371a7477'), max_length=260),
        ),
    ]
