# Generated by Django 3.0.3 on 2021-03-13 15:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0055_auto_20210313_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=['stuff', 'things'], size=None),
            preserve_default=False,
        ),
    ]