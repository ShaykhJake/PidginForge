# Generated by Django 3.0.3 on 2020-02-28 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='about',
            field=models.TextField(blank=True, default='', max_length=255, null=True),
        ),
    ]
