from django.db import models
from django.conf import settings
from categories.models import Language, TopicTag
from malapropos.models import Flag
from django.contrib.postgres.fields import ArrayField

class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    content = models.CharField(max_length=240)
    
    slug = models.SlugField(max_length=255, unique=True)
    
    nativelanguage = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="question_native_lanague", blank=True)
    learninglanguage = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="question_learning_language", blank=True)
    topic = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True, blank=True)
    tags = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    
    flag = models.ManyToManyField(Flag, blank=True, related_name="question_flag")
    suspended = models.BooleanField(default=False)
   #  comment = models.ManyToManyField(Comment, null=True)
    saved = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="question_saved")
    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="question_upvoted")
    downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="question_downvoted")


    def __str__(self):
        return self.author.username + ": " + self.content[:50] + '...'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    content = models.TextField()
    
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="votes")

    flag = models.ManyToManyField(Flag, blank=True, related_name="answer_flag")
    suspended = models.BooleanField(default=False)

    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="answer_upvoted")
    downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="answer_downvoted")

    def __str__(self):
        return self.author.username + ": " + self.content[:50] + '...'

class Reply(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="replies")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content = models.TextField()
    
    flag = models.ManyToManyField(Flag, blank=True, related_name="answer_reply_flag")
    suspended = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return self.author.username + ": " + self.content[:50] + '...'


