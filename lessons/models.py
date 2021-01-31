from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from categories.models import Language, TopicTag, MethodTag
from vocab.models import InflectedFormPair, VocabBank
from users.models import Profile
from malapropos.models import Flag
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from core.utils import generate_random_string

# Create your models here.


# lesson Model
class Lesson(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="lesson_curator")
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)

   title = models.CharField(max_length=140, default="new title", null=False)
   slug = models.SlugField(max_length=255, allow_unicode=True, unique=True, null=True, blank=True)
   objective = models.CharField(max_length=402, default="new objective", null=False)

   skill_level = models.CharField(max_length=32, default="Other", null=False)
   lesson_type = models.CharField(max_length=64, default="Other", null=False)

   source_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="lesson_native_language")
   target_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="lesson_target_language")
   topic = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True, related_name="lesson_topic")
   
   primary_vocab = models.ForeignKey(VocabBank, on_delete=models.SET_NULL, null=True, blank=True)

   citation = models.CharField(max_length=600, default="", null=True)

   published = models.BooleanField(default=False)
   content = JSONField(null=True, blank=True)

   saved = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="lesson_saved")
   hidden = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="lesson_hidden")

   flag = models.ManyToManyField(Flag, blank=True, related_name="lesson_flag")
   suspended = models.BooleanField(default=False)
   
   upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="lesson_upvoted")
   downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="lesson_downvoted")
   #  comment = models.ManyToManyField(Comment, null=True)

   def __str__(self):
      return self.title

@receiver(pre_save, sender=Lesson)
def add_slug_to_lesson(sender, instance, *args, **kwargs):
   if instance and not instance.slug:
      slugstring = instance.title
      slug = slugify(slugstring, allow_unicode=True)
      random_string = generate_random_string()
      instance.slug = slug + "-" + random_string

class LessonVocabBank(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
   word_pairs = models.ManyToManyField(InflectedFormPair)

   def __str__(self):
      return self.lesson.title