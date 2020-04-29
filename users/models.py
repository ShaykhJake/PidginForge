from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from categories.models import Language, TopicTag
# Create your models here.
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed


##### POINTS SCHEME ######
# 20 for first update of profile
# 10 for each like/save/upvote
# 20 for each follow
# 10 for posting a new element
# 20 for posting a new lesson
# 10 for each forked item
# 20 for establishing a study group


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    def add_email_address(self, request, new_email):
        # Add a new email address for the user, and send email confirmation.
        # Old email will remain the primary until the new one is confirmed.
        return EmailAddress.objects.add_email(request, self, new_email, confirm=True)

@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    # Once the email address is confirmed, make new email_address primary.
    # This also sets user.email to the new email address.
    # email_address is an instance of allauth.account.models.EmailAddress
    email_address.set_as_primary()
    # Get rid of old email addresses
    stale_addresses = EmailAddress.objects.filter(
        user=email_address.user).exclude(primary=True).delete()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    biography = models.TextField(max_length=255, default='', null=True, blank=True)
    country = models.TextField(max_length=100, default='', null=True, blank=True)
    geoloc = models.TextField(max_length=100, default='', null=True, blank=True)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/%Y/%m/%d')
    avatar = models.ImageField(default='avatars/default.jpg', upload_to='avatars/%Y/%m/%d')
    nativelanguage = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name='user_native_language')
    learninglanguage = models.ManyToManyField(Language, related_name='user_learning_language', blank=True)
    learningtopics = models.ManyToManyField(TopicTag, related_name='user_topics', blank=True)
    addedDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    followed = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="profile_followed")
    hidden = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="profile_hidden")
    points = models.IntegerField(default=0)

    # TODO
    # mentors
    # following (curators)
    # likedobjects = models.ManyToManyField(LearningObject, related_name='liked_objects')
    # savedobjects = models.ManyToManyField(LearningObject, related_name='saved_objects')

    # email_confirmed = models.BooleanField(default=False)

    # TODO s 
    # mentors
    # followed(creators)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super(Profile, self).save(*args, **kwargs)

def create_user(sender,instance,created,**kwargs):
    if created:
        # if CustomUser.username is NULL:
        #     CustomUser.username = "anonymous"
        Profile.objects.create(user=instance)

def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

post_save.connect(create_user, sender=CustomUser)
post_save.connect(create_auth_token, sender=CustomUser)

# @receiver(post_save, sender=CustomUser)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#         instance.profile.save()
