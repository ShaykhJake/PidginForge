# Generated by Django 3.0.3 on 2020-06-06 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('vocab', '0024_auto_20200606_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardstack',
            name='topics',
        ),
        migrations.AddField(
            model_name='cardstack',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.TopicTag'),
        ),
    ]
