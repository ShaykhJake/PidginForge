# Generated by Django 3.0.3 on 2020-05-17 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vocab', '0007_auto_20200517_1525'),
        ('lessons', '0003_auto_20200513_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonVocabBank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.Lesson')),
                ('word_pairs', models.ManyToManyField(null=True, to='vocab.InflectedFormPair')),
            ],
        ),
    ]
