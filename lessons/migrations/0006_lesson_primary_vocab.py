# Generated by Django 3.0.3 on 2020-05-21 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0009_auto_20200519_1131'),
        ('lessons', '0005_auto_20200517_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='primary_vocab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vocab.VocabBank'),
        ),
    ]