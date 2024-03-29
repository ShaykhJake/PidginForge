# Generated by Django 3.0.3 on 2021-03-17 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0011_auto_20210317_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savedlesson',
            old_name='curator',
            new_name='user',
        ),
        migrations.CreateModel(
            name='LessonHide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hides', to='lessons.Lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
