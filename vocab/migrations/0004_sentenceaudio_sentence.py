# Generated by Django 3.0.3 on 2020-05-17 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0003_auto_20200517_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentenceaudio',
            name='sentence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vocab.Sentence'),
        ),
    ]
