# Generated by Django 3.0.3 on 2020-06-06 13:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0046_auto_20200531_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='uid',
            field=models.CharField(default=uuid.UUID('5b23f585-f441-4329-9365-e0f46c4df845'), max_length=260),
        ),
    ]