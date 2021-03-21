from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from categories.models import Language, TopicTag, MethodTag
from users.models import Profile
from malapropos.models import Flag
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from core.utils import generate_random_string
import uuid


class CalendarEvent(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="event_curator") #do we want this to be null?
   # alternate_curators = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="alternate_event_curator")
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)

   name = models.CharField(max_length=140, default="", null=False)
   slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
   caption = models.CharField(max_length=320, default="", null=False)
   details = JSONField(null=True, blank=True)
   plain_text = models.TextField(default='', db_index=True)
   uid = models.CharField(max_length=260, default=uuid.uuid4())
   event_type = models.CharField(max_length=140, default="Meeting", null=False)
   native_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="event_native_language")
   target_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="event_target_language")
   tags = ArrayField(models.CharField(max_length=25), blank=True, null=True)
   all_day = models.BooleanField(default=False)   
   start_datetime = models.DateTimeField(editable=True)
   end_datetime = models.DateTimeField(editable=True)

   location = models.CharField(max_length=128, default="", null=True)

   public = models.BooleanField(default=True)
   guest_list = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="invited_event_guest")
   parent_event = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="recurrence")


   def __str__(self):
      return self.name + " " + self.start_datetime.strftime("%m/%d/%Y")

@receiver(pre_save, sender=CalendarEvent)
def add_slug_to_calendarevent(sender, instance, *args, **kwargs):
   if instance and not instance.slug:
      slugstring = instance.name + "_" + instance.start_datetime.strftime("%m/%d/%Y")
      slug = slugify(slugstring)
      random_string = generate_random_string()
      instance.slug = slug + "-" + random_string

@receiver(pre_save, sender=CalendarEvent)
def add_uid_to_calendarevent(sender, instance, *args, **kwargs):
   if instance and not instance.uid:
      uid = uuid.uuid4()
      instance.uid = uid


class EventRSVP(models.Model):
   RSVP_RESPONSE = [
      ('Yes', 'Yes'),
      ('Maybe', 'Maybe'),
      ('No', 'No'),
   ]
   invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name="invited_user")
   event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE, null=False, related_name="rsvp")
   attending = models.CharField(max_length=10, choices=RSVP_RESPONSE, default='Yes', null=False)
   comment = models.CharField(max_length=255, default="", null=False)
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)

   def __str__(self):
      # return self.invited_user.username + " - " + self.event.name
      return self.invited_user.username + " RSVPd to " + self.event.name

class EventAttendee(models.Model):
   attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name="event_attendee")
   event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE, null=False, related_name="attendees")

class EventComment(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name="event_comment_curator")
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE, null=False, related_name="comment")
   content = JSONField(null=True, blank=True)

class CommentReply(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name="event_comment_reply_curator")
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   parent_comment = models.ForeignKey(EventComment, on_delete=models.CASCADE, null=False, related_name="comment_reply")
   content = JSONField(null=True, blank=True)



# class Attendee(models.Model):
#    user =
#    event =
#    pass


