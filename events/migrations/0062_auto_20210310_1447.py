# Generated by Django 3.0.3 on 2021-03-10 14:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0061_auto_20210309_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('817eee89-d75f-4087-b28e-3e52512e33bf'), max_length=260),
        ),
    ]
