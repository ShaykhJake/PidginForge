# Generated by Django 3.0.3 on 2021-03-13 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elements', '0053_auto_20210313_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementUpVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Element')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_upvotes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ElementSave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Element')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_saves', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ElementHide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Element')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_hides', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ElementDownVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elements.Element')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element_downvotes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]