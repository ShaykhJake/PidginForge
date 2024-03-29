# Generated by Django 3.0.3 on 2021-03-13 11:46

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0048_element'),
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elements.Element')),
                ('rich_text', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('plain_text', models.TextField(default='')),
            ],
            bases=('elements.element',),
        ),
    ]
