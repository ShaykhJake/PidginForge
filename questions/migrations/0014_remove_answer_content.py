# Generated by Django 3.0.3 on 2021-03-10 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_remove_question_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='content',
        ),
    ]