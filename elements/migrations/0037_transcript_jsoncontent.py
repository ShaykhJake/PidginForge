# Generated by Django 3.0.3 on 2020-04-20 16:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0036_auto_20200419_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='jsoncontent',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
