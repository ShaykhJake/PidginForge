from django.db import models
from django.conf import settings
# Create your models here.

   #  malapropos = models.ManyToManyField(Malapropos, related_name="YT_malapropos", null=True)
   #  comment = models.ManyToManyField(Comment, related_name="YT_comment", null=True)
   #  saved = models.ManyToManyField(Comment, related_name="YT_comment", null=True)
   #  upvote = models.ManyToManyField(Comment, related_name="YT_comment", null=True)
   #  downvote= models.ManyToManyField(Comment, related_name="YT_comment", null=True)

class Malapropos(models.Model):
    COPYRIGHT = 'COP'
    OFFENSIVE = 'OFF'
    FLAGREASON = [
        (COPYRIGHT, 'Copyright'),
        (OFFENSIVE, 'Offensive'),
    ]
    reason = models.CharField(max_length=3,choices=FLAGREASON,default=COPYRIGHT)
    justification = models.CharField(max_length=300, default="", null=False)
    flagger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

class Comment(models.Model):
   pass

class Saved(models.Model):
   pass

class UpVote(models.Model):
   pass

class DownVote(models.Model):
   pass

