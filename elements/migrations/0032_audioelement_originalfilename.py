# Generated by Django 3.0.3 on 2020-04-17 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elements', '0031_audioelement_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='audioelement',
            name='originalfilename',
            field=models.CharField(default='', max_length=200),
        ),
    ]
