# Generated by Django 3.0.3 on 2021-03-17 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0015_lesson_plain_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='downvote',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='hidden',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='saved',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='upvote',
        ),
    ]