from django.db import models
from django.conf import settings


# Create your models here.
class Forum(models.Model):
  active = models.BooleanField(default=True)
  name = models.CharField(max_length=150)
  description = models.CharField(max_length=300)
  curation_date = models.DateTimeField(auto_now_add=True)
  # language 

  def __str__(self):
    return self.name

class Moderator(models.Model):
  forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Thread(models.Model):
  locked = models.BooleanField(default=False)
  # sticky = models.BooleanField(default=False)
  active = models.BooleanField(default=True)
  subject = models.CharField(max_length=250)
  forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
  views = models.PositiveIntegerField(default=0)
  curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  curation_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.subject} - {self.forum.name}"

class ThreadFollower(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

class Post(models.Model):
  quoted = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='quotes')
  message = models.TextField()
  quoted_text = models.TextField(null=True, blank=True)
  curation_date = models.DateTimeField(auto_now_add=True)
  curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
  parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

  def __str__(self):
    return (
      f"{self.curation_date.strftime('%Y-%m-%d')} by "
      f"{self.curator.username}: "
      f"'{self.message[0:30]}...'"
    )

"""
I think that for this one I might end up creating individual actions...not sure

class ModeratorAction(models.Model):
  moderator = models.ForeignKey(User, on_delete=models.CASCADE)
  description = models.CharField(max_length="200")
  forum = models.models.ForeignKey(Forum, on_delete=models.CASCADE)
  user = 
  thread = models.ForeignKey(Thread, on_delete=)

"""