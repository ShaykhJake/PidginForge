from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

DIRECTION_CHOICES = (
    ('LTR', 'LTR'),
    ('RTL', 'RTL'),
)

class Language(models.Model):
    name = models.CharField(max_length=200, unique=True)
    trigraph = models.CharField(max_length=10, unique=True)
    direction = models.CharField(max_length=5, choices = DIRECTION_CHOICES, default = 'LTR')

    def __str__(self):
        return self.name

class MethodTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class TopicTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
