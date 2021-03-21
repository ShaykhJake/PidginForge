from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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



"""Here we need to create a generic model for a comment, which can then be inherited"""

"""
class Comment(models.Model):
   curator = models.ForeignKey(User, on_delete=models.CASCADE)
   body = models.TextField()
   curation_date = models.DateTimeField(auto_now_add=True)
   parent = models.ForeignKey(self, null=True, related_name='children')

   class Meta:
      abstract = True

class VideoComment(Comment):
   pass

class AudioComment(Comment):
   pass

class TextComment(Comment):
   pass

class LessonComment(Comment):
   pass

class StackComment(Comment):
   pass

class 
"""

"""
If i made this an abstract base class instead, then each type model can simply refer to comments =...each comment
would have its own PK and be able to refer to another comment's PK for nesting...


class Comment(models.Model):
    curator = models.ForeignKey(User)
    body = JSON...
    parent = Self-reference
    curation_date = models.DateTimeField(auto_now_add=True)
   #  activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = 

    # Below are the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

#EXAMPLE:
class YouTubeElement(models.Model):
    ...
    comments = GenericRelation(Activity)
    ...


"""




class Saved(models.Model):
   pass

class UpVote(models.Model):
   pass

class DownVote(models.Model):
   pass

