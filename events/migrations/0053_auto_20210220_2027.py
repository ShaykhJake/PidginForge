# Generated by Django 3.0.3 on 2021-02-20 20:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0052_auto_20210131_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('92069106-afe1-4867-9968-d1a0086e0b58'), max_length=260),
        ),
    ]