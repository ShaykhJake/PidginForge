# Generated by Django 3.0.3 on 2020-02-22 14:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='voters',
            field=models.ManyToManyField(related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
    ]
