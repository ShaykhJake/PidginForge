# Generated by Django 3.0.3 on 2021-03-22 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0067_commentreply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcript',
            name='downvote',
        ),
        migrations.RemoveField(
            model_name='transcript',
            name='translations',
        ),
        migrations.RemoveField(
            model_name='transcript',
            name='upvote',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='downvote',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='upvote',
        ),
        migrations.AddField(
            model_name='transcript',
            name='plain_text',
            field=models.TextField(db_index=True, default=''),
        ),
        migrations.AddField(
            model_name='translation',
            name='plain_text',
            field=models.TextField(db_index=True, default=''),
        ),
    ]
