# Generated by Django 3.0.3 on 2020-05-13 13:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('malapropos', '0003_flag_reason'),
        ('lessons', '0002_auto_20200512_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='downvote',
            field=models.ManyToManyField(blank=True, related_name='lesson_downvoted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='flag',
            field=models.ManyToManyField(blank=True, related_name='lesson_flag', to='malapropos.Flag'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='hidden',
            field=models.ManyToManyField(blank=True, related_name='lesson_hidden', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='saved',
            field=models.ManyToManyField(blank=True, related_name='lesson_saved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='suspended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lesson',
            name='upvote',
            field=models.ManyToManyField(blank=True, related_name='lesson_upvoted', to=settings.AUTH_USER_MODEL),
        ),
    ]