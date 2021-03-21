# Generated by Django 3.0.3 on 2021-01-15 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0026_remove_cardstack_custom_cards'),
        ('lessons', '0008_auto_20200524_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='primary_vocab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vocab.VocabBank'),
        ),
    ]