# Generated by Django 3.0.3 on 2020-05-01 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20200501_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventrsvp',
            name='comment',
            field=models.CharField(default='', max_length=255),
        ),
    ]