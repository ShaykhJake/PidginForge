# Generated by Django 3.0.3 on 2020-04-08 16:20

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('questions', '0002_answer_voters'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='learninglanguage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_learning_language', to='categories.Language'),
        ),
        migrations.AddField(
            model_name='question',
            name='nativelanguage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_native_lanague', to='categories.Language'),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None),
        ),
    ]
