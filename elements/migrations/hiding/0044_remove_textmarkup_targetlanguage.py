# Generated by Django 3.0.3 on 2020-04-28 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0043_auto_20200428_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textmarkup',
            name='markuplanguage',
        ),
    ]