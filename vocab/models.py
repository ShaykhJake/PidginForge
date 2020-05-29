from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from categories.models import Language, TopicTag, MethodTag
from elements.models import AudioElement, TextElement, YouTubeElement
from malapropos.models import Flag
# from interactions.models import Rating
# from interactions.models import Saved, Upvote, Downvote, Comment, Malapropos
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from core.utils import generate_random_string


### ROOTS
class WordRoot(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   root = models.CharField(max_length=128, default="", null=False)
   languages = models.ManyToManyField(Language)
   
   def __str__(self):
      return self.root


### LEXEMES
class Lexeme(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   language = models.ForeignKey(Language, on_delete=models.CASCADE, null=False)
   lemma = models.CharField(max_length=255, default="", null=False)
   curator_note = models.CharField(max_length=255, default="", null=False)
   slug = models.SlugField(allow_unicode=True, max_length=255, unique=True, null=True, blank=True)
   
   def __str__(self):
      return self.lemma


@receiver(pre_save, sender=Lexeme)
def add_slug_to_lesson(sender, instance, *args, **kwargs):
   if instance and not instance.slug:
      slugstring = instance.language.name + "-" + instance.lemma
      slug = slugify(slugstring, allow_unicode=True)
      random_string = generate_random_string()
      instance.slug = slug + "-" + random_string


class LexemeGrammar(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   part_of_speech = models.CharField(max_length = 64)
   lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE, null=False)
   language = models.ForeignKey(Language, on_delete=models.CASCADE, null=False)
   content = models.TextField(default="", null=False)
   rich_content = JSONField(null=True, blank=True)

   def __str__(self):
      return self.lexeme.lemma + ' - ' + self.content

class LexemeDefinition(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE, null=False)
   language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
   content = models.TextField(default="", null=False)
   part_of_speech = models.CharField(max_length=255, default="n/a", null=False)
   source_name = models.CharField(max_length=255, default="n/a", null=True)
   source_citation = models.TextField(default="n/a", null=True)

   def __str__(self):
      return self.lexeme.lemma + ' - ' + self.content

class LexemePronunciation(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   text = models.TextField()
   lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE, null=False)
   audio_file = models.FileField(null=True, upload_to='vocab/lexemes/pronunciation/%Y/%m/%d')

   def __str__(self):
      return self.lexeme.lemma + ' - ' + self.text

class LexemeRoot(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
   root = models.ForeignKey(WordRoot, on_delete=models.CASCADE)

   def __str__(self):
      return self.lexeme.lemma + ' - ' + self.root.root


### INFLECTIONS
class InflectedForm(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   lexeme = models.ForeignKey(Lexeme, on_delete=models.SET_NULL, null=True)
   language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
   word = models.CharField(max_length=255)
   curator_note = models.CharField(max_length=255, default="", null=False)

   def __str__(self):
      return self.word

class InflectedFormGrammar(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   inflected_form = models.ForeignKey(InflectedForm, on_delete=models.CASCADE, null=False)
   language = models.ForeignKey(Language, on_delete=models.CASCADE)
   content = models.TextField(default="", null=False)
   rich_content = JSONField(null=True, blank=True)

   def __str__(self):
      return self.inflected_form.word + ' - ' + self.content

class InflectedFormDefinition(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   inflected_form = models.ForeignKey(InflectedForm, on_delete=models.CASCADE, null=False)
   language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
   definition = models.TextField(default="", null=False)
   source_name = models.CharField(max_length=255, default="n/a", null=True)
   source_citation = models.TextField(default="n/a", null=True)

   def __str__(self):
      return self.inflected_form.word + ' - ' + self.definition


class InflectedFormPronunciation(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   text = models.CharField(max_length=128)
   inflected_form = models.ForeignKey(InflectedForm, on_delete=models.CASCADE, null=False)
   audio_file = models.FileField(upload_to='vocab/inflected_forms/pronunciation/%Y/%m/%d')
   curator_note = models.TextField(default="", null=True)

   def __str__(self):
      return self.inflected_form.word + ' - ' + self.text


class InflectedFormImage(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   inflected_form = models.ForeignKey(InflectedForm, on_delete=models.CASCADE, null=False)
   image_file = models.ImageField(upload_to='vocab/inflected_forms/images/%Y/%m/%d')
   curator_note = models.CharField(max_length=255, default="", null=True)

### SENTENCES 
class Sentence(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
   topic = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True)
   text = models.TextField(default="", null=False)
   curator_note = models.CharField(max_length=255, default="", null=True)

   def __str__(self):
      return self.text

class SentenceTranslation(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True) #do we want this to be null?
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
   language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
   text = models.TextField(default="", null=False)
   curator_note = models.CharField(max_length=255, default="", null=True)
   
   def __str__(self):
      return self.text

class SentenceAudio(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, null=True)
   audiofile = models.FileField(upload_to='vocab/sentences/audio/%Y/%m/%d')
   curator_note = models.CharField(max_length=255, default="", null=True)

class InflectedFormSentence(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   inflected_form = models.ForeignKey(InflectedForm, on_delete=models.CASCADE)
   sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)

   def __str__(self):
      return self.inflected_form.word + ' - ' + self.sentence.text



### PAIRINGS
class LexemePair(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   lexeme_1 = models.ForeignKey(Lexeme, on_delete=models.CASCADE, related_name="lexeme_pair_1")
   lexeme_2 = models.ForeignKey(Lexeme, on_delete=models.CASCADE, related_name="lexeme_pair_2")
   curator_note = models.CharField(max_length=255, default="", null=True)

   def __str__(self):
      return self.lexeme_1.lemma + ' - ' + self.lexeme_2.lemma


class InflectedFormPair(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   inflected_form_1 = models.ForeignKey(InflectedForm, on_delete=models.CASCADE, related_name="inflected_form_pair_1")
   inflected_form_2 = models.ForeignKey(InflectedForm, on_delete=models.CASCADE, related_name="inflected_form_pair_2")
   curator_note = models.CharField(max_length=255, default="", null=True)

   def __str__(self):
      return self.inflected_form_1.word + ' - ' + self.inflected_form_2.word



# class Confusable(models.Model):
#    inflected_form_1
#    inflected_form_2

# class Synonyms(models.Model):
#    lexeme_1
#    lexeme_2

# class Antonyms(models.Model):
#    lexeme_1
#    lexeme_2

### VOCAB BANKS, LISTS, & CARDS
# class VocabBankItem(models.Model):
#    word_pair = models.ManyToManyField(InflectedFormPair)
   
class VocabBank(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   word_pairs = models.ManyToManyField(InflectedFormPair)

# class LexemeLearning(models.Model):
#    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="attached_note_curator") #do we want this to be null?
#    curationdate = models.DateTimeField(auto_now_add=True, editable=False)
#    learning_lexeme = models.ForeignKey(Lexeme)
#    known_lexeme = models.ForeignKey(Lexeme)
#    last_attempted = models.DateTimeField(auto_now=True, editable=False)
#    attempts = models.PositiveIntegerField(default=0)
#    number_correct = models.PositiveIntegerField(default=0)
#    active = models.BooleanField(default=True)

# class CardStack(models.Model):
#    # presentation of words in vocab games will be calculated by
#    # user preference and what pairs are available. 
#    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="attached_note_curator") #do we want this to be null?
#    curationdate = models.DateTimeField(auto_now_add=True, editable=False)
#    updated = models.DateTimeField(auto_now=True, editable=False)
#    name = models.CharField(max_length=305, default="", null=False)
#    public = models.BooleanField(default=False)
#    topics = models.ManyToManyField(TopicTag)
#    learning_languages = models.ManyToManyField(Language)
#    lexeme_pairs = models.ManyToManyField(LexemePair)

#    # TODO CREATE A SLUG FOR THIS CARD STACK!?
#    # most statistics will be calculated by individual stack
