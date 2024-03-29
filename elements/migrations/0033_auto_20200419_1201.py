# Generated by Django 3.0.3 on 2020-04-19 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elements', '0032_audioelement_originalfilename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translation',
            name='transcript',
        ),
        migrations.AddField(
            model_name='transcript',
            name='downvote',
            field=models.ManyToManyField(blank=True, related_name='transcript_downvoted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transcript',
            name='forkparent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forks', to='elements.Transcript'),
        ),
        migrations.AddField(
            model_name='transcript',
            name='translation',
            field=models.ManyToManyField(blank=True, related_name='transcripts', to='elements.Translation'),
        ),
        migrations.AddField(
            model_name='transcript',
            name='upvote',
            field=models.ManyToManyField(blank=True, related_name='transcript_upvoted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='translation',
            name='downvote',
            field=models.ManyToManyField(blank=True, related_name='translation_downvoted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='translation',
            name='forkparent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forks', to='elements.Translation'),
        ),
        migrations.AddField(
            model_name='translation',
            name='upvote',
            field=models.ManyToManyField(blank=True, related_name='translation_upvoted', to=settings.AUTH_USER_MODEL),
        ),
    ]
