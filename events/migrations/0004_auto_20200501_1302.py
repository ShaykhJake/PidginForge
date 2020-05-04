# Generated by Django 3.0.3 on 2020-05-01 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_commentreply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarevent',
            name='parent_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recurrence', to='events.CalendarEvent'),
        ),
    ]