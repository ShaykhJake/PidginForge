# Generated by Django 3.0.3 on 2021-03-17 15:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0013_auto_20210317_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='content',
        ),
        migrations.AddField(
            model_name='lesson',
            name='rich_text',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]