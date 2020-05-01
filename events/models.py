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


class CalendarEvent(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="event_curator") #do we want this to be null?
   # alternate_curators = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="alternate_event_curator")
   curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   updated = models.DateTimeField(auto_now=True, editable=False)

   name = models.CharField(max_length=140, default="", null=False)
   slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
   caption = models.CharField(max_length=320, default="", null=False)
   details = JSONField(null=True, blank=True)

   event_type = models.CharField(max_length=140, default="Meeting", null=False)
   native_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="event_native_language")
   target_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="event_target_language")
   topic = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True, related_name="event_topic")
   
   start = models.DateTimeField(editable=True)
   end = models.DateTimeField(editable=True)
   location = models.CharField(max_length=128, default="", null=True)

   public = models.BooleanField(default=True)
   parent_event = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="recurrence")

   def __str__(self):
      return self.name + " " + self.start.strftime("%m/%d/%Y")

@receiver(pre_save, sender=CalendarEvent)
def add_slug_to_calendarevent(sender, instance, *args, **kwargs):
   if instance and not instance.slug:
      slugstring = instance.name + "_" + instance.start.strftime("%m/%d/%Y")
      slug = slugify(slugstring)
      random_string = generate_random_string()
      instance.slug = slug + "-" + random_string

class UserInvite(models.Model):
   invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name="event_invited_user")
   event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE, null=False, related_name="user_invite")

   def __str__(self):
      # return self.invited_user.username + " - " + self.event.name
      return self.invited_user.username + " was invited to " + self.event.name + " on " + self.event.start.strftime("%m/%d/%Y") + " at " + self.event.start.strftime("%H:%M")

# class StudyGroupInvite(models.Model):
#    invited_user = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=False, related_name="event_invited_group")
#    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE, null=False, related_name="group_invite")

# class ClassInvite(models.Model):
#    pass

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


