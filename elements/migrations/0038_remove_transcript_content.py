# Generated by Django 3.0.3 on 2020-04-20 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0037_transcript_jsoncontent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcript',
            name='content',
        ),
    ]
