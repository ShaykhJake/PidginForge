from django.db import models
from django.conf import settings
from categories.models import Language, TopicTag
from malapropos.models import Flag
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils.text import slugify
from core.utils import generate_random_string

class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150)
    rich_text = JSONField(null=True, blank=True)
    plain_text = models.TextField(default='', db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    nativelanguage = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="question_native_lanague", blank=True)
    learninglanguage = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="question_learning_language", blank=True)
    tags = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    flag = models.ManyToManyField(Flag, blank=True, related_name="question_flag")
    suspended = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.title[:50]
            slug = slugify(value, allow_unicode=True)
            random_string = generate_random_string()
            self.slug = slug + "-" + random_string
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author.username} - {self.title}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    details = JSONField(null=True, blank=True)
    flag = models.ManyToManyField(Flag, blank=True, related_name="answer_flag")
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author.username}"

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

class QuestionComment(models.Model):
    answer = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content = models.TextField()
    
    flag = models.ManyToManyField(Flag, blank=True, related_name="question_comment_flags")
    suspended = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return self.author.username + ": " + self.content[:50] + '...'

class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="comments")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content = models.TextField()
    
    flag = models.ManyToManyField(Flag, blank=True, related_name="answer_comment_flags")
    suspended = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return self.author.username + ": " + self.content[:50] + '...'


class QuestionUpVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="question_upvotes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="upvotes")

class QuestionDownVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="question_downvotes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="downvotes")

class QuestionSave(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="question_saves")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="saves")

class QuestionHide(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="question_hides")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="hides")

class AnswerUpVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answer_upvotes")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="upvotes")

class AnswerDownVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answer_downvotes")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="downvotes")

