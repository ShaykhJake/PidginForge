from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from categories.models import Language, TopicTag, MethodTag
from users.models import Profile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from core.utils import generate_random_string
# Create your models here.



def group_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'studygroups/{0}/{1}'.format(instance.id, filename)

class StudyGroup(models.Model):
   founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="study_group_founder")
   # alternate_curators = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="alternate_event_curator")
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)
   # image = models.ImageField(default='study_group/images/default.jpg', upload_to='study_group/images/%Y/%m/%d')
   image = models.ImageField(default='study_group/images/default.jpg', upload_to=group_directory_path)

   name = models.CharField(max_length=140, default="", null=False)
   slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
   caption = models.CharField(max_length=320, default="", null=False)
   details = JSONField(null=True, blank=True)

   native_languages = models.ManyToManyField(Language, null=True, related_name="study_group_native_language")
   target_languages = models.ManyToManyField(Language, null=True, related_name="study_group_target_language")
   topics = models.ManyToManyField(TopicTag, null=True, related_name="study_group_topic")
   
   visibility = models.BooleanField(default=True)
   open_registration = models.BooleanField(default=False)

   def __str__(self):
      return self.name

@receiver(pre_save, sender=StudyGroup)
def add_slug_to_studygroup(sender, instance, *args, **kwargs):
   if instance and not instance.slug:
      slugstring = instance.name
      slug = slugify(slugstring)
      random_string = generate_random_string()
      instance.slug = slug + "-" + random_string

class GroupMember(models.Model):
   MEMBER_TYPES = [
      # Admin can make changes to the group itself
      (4, 'Admin'),
      # Moderators can approve members, suspend members, add events, and moderate comments
      (3, 'Moderator'),
      # General can add comments and participate in a general fashion
      (2, 'General'),
      # Auditors can only view group content
      (1, 'Auditor'),
      # Suspension removes user access
      (0, 'Suspended'),
   ]
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_group_member")
   group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name="member")
   member_type = models.PositiveIntegerField(max_length=1, choices=MEMBER_TYPES, default=2)
   join_date = models.DateTimeField(auto_now_add=True, editable=False)
   active = models.BooleanField(default=True) 
