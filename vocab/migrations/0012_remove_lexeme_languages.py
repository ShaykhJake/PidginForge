# Generated by Django 3.0.3 on 2020-05-24 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0011_auto_20200524_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lexeme',
            name='languages',
        ),
    ]
