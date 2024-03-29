# Generated by Django 3.0.3 on 2020-05-17 13:14

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InflectedForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('word', models.CharField(max_length=640)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lexeme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lemma', models.CharField(default='', max_length=255)),
                ('primary_definition', models.TextField(default='')),
                ('curator_note', models.CharField(default='', max_length=255)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('languages', models.ManyToManyField(to='categories.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(default='')),
                ('curator_note', models.CharField(default='', max_length=255)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.Language')),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.TopicTag')),
            ],
        ),
        migrations.CreateModel(
            name='WordRoot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('root', models.CharField(default='', max_length=128)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('languages', models.ManyToManyField(to='categories.Language')),
            ],
        ),
        migrations.CreateModel(
            name='SentenceTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(default='')),
                ('curator_note', models.CharField(default='', max_length=255)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.Language')),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.Sentence')),
            ],
        ),
        migrations.CreateModel(
            name='SentenceAudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('audiofile', models.FileField(upload_to='vocab/sentences/audio/%Y/%m/%d')),
                ('curator_note', models.CharField(default='', max_length=255)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attached_note_curator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LexemeRoot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('lexeme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.Lexeme')),
                ('root', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.WordRoot')),
            ],
        ),
        migrations.CreateModel(
            name='LexemePronunciation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('audio_file', models.FileField(upload_to='')),
                ('curator_note', models.CharField(default='', max_length=255)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('lexeme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.Lexeme')),
            ],
        ),
        migrations.CreateModel(
            name='LexemeGrammar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('part_of_speech', models.CharField(max_length=64)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Language')),
                ('lexeme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.Lexeme')),
            ],
        ),
        migrations.CreateModel(
            name='LexemeDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(default='')),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.Language')),
                ('lexeme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.Lexeme')),
            ],
        ),
        migrations.CreateModel(
            name='InflectedFormSentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('inflected_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.InflectedForm')),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.Sentence')),
            ],
        ),
        migrations.CreateModel(
            name='InflectedFormPronunciation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=128)),
                ('audio_file', models.FileField(upload_to='vocab/inflected_forms/pronunciation/%Y/%m/%d')),
                ('curator_note', models.TextField(default='')),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('inflected_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.InflectedForm')),
            ],
        ),
        migrations.CreateModel(
            name='InflectedFormImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image_file', models.ImageField(upload_to='vocab/inflected_forms/images/%Y/%m/%d')),
                ('curator_note', models.CharField(default='', max_length=255)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('inflected_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.InflectedForm')),
            ],
        ),
        migrations.CreateModel(
            name='InflectedFormGrammar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('inflected_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.InflectedForm')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Language')),
            ],
        ),
        migrations.CreateModel(
            name='InflectedFormDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curationdate', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('definition', models.TextField(default='')),
                ('curator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('inflected_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocab.InflectedForm')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.Language')),
            ],
        ),
    ]
