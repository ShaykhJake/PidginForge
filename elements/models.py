from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from categories.models import Language, TopicTag, MethodTag
from malapropos.models import Flag
# from interactions.models import Rating
# from interactions.models import Saved, Upvote, Downvote, Comment, Malapropos
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from core.utils import generate_random_string


class Translation(models.Model):
    # Source & User
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="translation_curator") #do we want this to be null?
    targetlanguage = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    
    curationdate = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    
    #### Content
    content = JSONField(null=True, blank=True)
    notes = models.TextField(default='', null=True, blank=True)
    # REFERENCES
    # TODO termlist = models.ManyToMany  ... #Should we store the list of words here, or create a separate list with a key to it?
    # TODO speakers = models.ManyToManyField(Person, related_name="transcript_speaker")
    # TODO people = models.ManyToManyField(Person, related_name="transcript_reference")
    # TODO placenames = models.ManyToManyField(PlaceName, related_name="transcript_placename")
    # TODO termpairs = ... THIS IS A WAY FOR THE TRANSLATOR TO HIGHLIGHT RELATIONSHIPS BETWEEN TRANSLATED TERMS AND TRANSCRIPT TERMS

    # Interactions
    published = models.BooleanField(default=False)
    forkparent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='forks')
    # TODO Figure out the QC models...this might be a bit more complicated because of
    # how to track & integrate changes that were previously made
    # TODO qcs = models.ManyToManyField... #Should this be totally separate?


    # TODO Build Interactions
    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="translation_upvoted")
    downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="translation_downvoted")

    # TODO add something in here about forking?? QCing?
    #  Interactions
    
    def __str__(self):
        if (self.curator and self.targetlanguage):
            return self.curator.username + " on " + self.curationdate.strftime("%B %d, %Y") + " in " + self.targetlanguage.name 
        else:
            return "Object Orphaned"


class Transcript(models.Model):
    ## This model is a critical many-to-many model; resource: https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/
    # Source & User
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="transcript_curator") #do we want this to be null?
    curationdate = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)
   
    #### Content
    content = JSONField(null=True, blank=True)
    notes = models.TextField(default='', null=True, blank=True)
    # References #TODO
    # TODO termlist = models.ManyToMany  ... #Should we store the list of words here, or create a separate list with a key to it?
    # TODO speakers = models.ManyToManyField(Person, related_name="transcript_speaker")
    # TODO people = models.ManyToManyField(Person, related_name="transcript_reference")
    # TODO placenames = models.ManyToManyField(PlaceName, related_name="transcript_placename")

    # QCing & Forking #TODO
    published = models.BooleanField(default=False)
    forkparent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='forks')
    # TODO Figure out the QC models...this might be a bit more complicated because of
    # how to track & integrate changes that were previously made
    # TODO qcs = models.ManyToManyField... #Should this be totally separate?
    
    #  Interactions #TODO 
    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="transcript_upvoted")
    downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="transcript_downvoted")
    # HOW TO ADD COMMENT FLAGS DIRECTLY TO SCRIPT????!? TODO

    translations = models.ManyToManyField(Translation, blank=True, related_name="transcripts")
    #  rating = models.ManyToManyField(Rating, null=True)
    #  comment = models.ManyToManyField(Comment, null=True)

    def __str__(self):
        if (self.curator):
            return self.curator.username + " on " + self.curationdate.strftime("%B %d, %Y")
        return "Object Orphaned"



class YouTubeElement(models.Model):
    # Curation Info
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="youtube_curator")
    curationdate = models.DateTimeField(auto_now_add=True, editable=False)
    transcripts = models.ManyToManyField(Transcript, blank=True, related_name="youtube_transcripts")

    purpose = models.CharField(max_length=305, default="", null=False)
    notes = models.CharField(max_length=305, default="", null=False, blank=True)

    # YouTube Source Info
    videoid = models.CharField(max_length=100, null=True, blank=True)
    thumbURL = models.CharField(max_length=200, null=True, blank=True)
    
    # Length will be stored in seconds, then converted into HH:MM:SEC for display by the browser
    duration = models.PositiveIntegerField(default=0) 

    # Title Defaults to What's Pulled in From YouTube, but Can be Changed
    title = models.CharField(max_length=150, default="", null=False)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    # TODO - Consider whether or not to add a start/stop time?

    # Categories
    topic = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    tags = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    # TODO minorlanguage = models.ManyToManyField(Language)
    
    # Views is simply a one-up calculation every time a YTElement is loaded for viewing (TODO)
    views = models.PositiveIntegerField(default=0, editable=False)
    
   #  Interactions
    saved = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="youtube_saved")
    hidden = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="youtube_hidden")
   #  rating = models.ManyToManyField(Rating, null=True)
    flag = models.ManyToManyField(Flag, blank=True, related_name="youtube_flag")
    suspended = models.BooleanField(default=False)
   #  comment = models.ManyToManyField(Comment, null=True)

    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="youtube_upvoted")
    downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="youtube_downvoted")


    def __str__(self):
        return self.title
    
    def short(self):
        return self.purpose[:250] + '...'

    # TODO Is this still needed?
    def get_absolute_url(self):
        return reverse("youtubelement-detail", kwargs={"pk": self.pk})


@receiver(pre_save, sender=YouTubeElement)
def add_slug_to_youtubeelement(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.title)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string

class AudioElement(models.Model):
    # Curation Info
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="audio_curator")
    curationdate = models.DateTimeField(auto_now_add=True, editable=False)
    transcripts = models.ManyToManyField(Transcript, editable=False)

    purpose = models.CharField(max_length=305, default="", null=False)
    notes = models.CharField(max_length=305, default="", null=False, blank=True)

    # Audio Cut Info
    audiofile = models.FileField(upload_to='audio_files/%Y/%m/%d')
    originalfilename = models.CharField(max_length=200, default="", null=False)
    citation = models.CharField(max_length=305, default="", null=False)
    
    # Length will be stored in seconds, then converted into HH:MM:SEC for display by the browser
    duration = models.PositiveIntegerField(default=0)

    # Title Defaults to What's Pulled in From YouTube, but Can be Changed
    title = models.CharField(max_length=150, default="", null=False)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    # TODO - Consider whether or not to add a start/stop time?

    # Categories
    topic = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    tags = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    # TODO minorlanguage = models.ManyToManyField(Language)
    
    # Views is simply a one-up calculation every time a YTElement is loaded for viewing (TODO)
    views = models.PositiveIntegerField(default=0, editable=False)
    
   #  Interactions
    saved = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="audio_saved")
    hidden = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="audio_hidden")
   #  rating = models.ManyToManyField(Rating, null=True)
    flag = models.ManyToManyField(Flag, blank=True, related_name="audio_flag")
    suspended = models.BooleanField(default=False)
   #  comment = models.ManyToManyField(Comment, null=True)

    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="audi_upvoted")
    downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="audi_downvoted")


    def __str__(self):
        return self.title
    
    def short(self):
        return self.purpose[:250] + '...'

    # TODO Is this still needed?
    def get_absolute_url(self):
        return reverse("audio-detail", kwargs={"pk": self.pk})


@receiver(pre_save, sender=AudioElement)
def add_slug_to_audioelement(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.title)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string


class TextMarkup(models.Model):
    ## This model is a critical many-to-many model; resource: https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/
    # Source & User
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="textmarkup_curator") #do we want this to be null?
    curationdate = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)
   
    #### Content
    content = JSONField(null=True, blank=True)
    notes = models.TextField(default='', null=True, blank=True)
    
    targetlanguage = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name="markup_target")
    # References #TODO
    # TODO termlist = models.ManyToMany  ... #Should we store the list of words here, or create a separate list with a key to it?
    # TODO speakers = models.ManyToManyField(Person, related_name="transcript_speaker")
    # TODO people = models.ManyToManyField(Person, related_name="transcript_reference")
    # TODO placenames = models.ManyToManyField(PlaceName, related_name="transcript_placename")

    # QCing & Forking #TODO
    published = models.BooleanField(default=False)
    forkparent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='forks')
    # TODO Figure out the QC models...this might be a bit more complicated because of
    # how to track & integrate changes that were previously made
    # TODO qcs = models.ManyToManyField... #Should this be totally separate?
    
    #  Interactions #TODO 
    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="markup_upvoted")
    downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="markup_downvoted")
    # HOW TO ADD COMMENT FLAGS DIRECTLY TO SCRIPT????!? TODO

    def __str__(self):
        if (self.curator):
            return self.curator.username + " on " + self.curationdate.strftime("%B %d, %Y")
        return "Object Orphaned"


class TextElement(models.Model):
    ## This model is a critical many-to-many model; resource: https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/
    # Source & User
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="text_curator") #do we want this to be null?
    curationdate = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)
   
    #### Content
    title = models.CharField(max_length=150, default="", null=False)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    content = JSONField(null=True, blank=True)
    rawtext = models.TextField(default='')
    charactercount = models.PositiveIntegerField(default=0)

    topic = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    purpose = models.CharField(max_length=305, default="", null=False)
    
    citation = models.CharField(max_length=305, default="", null=False)
    notes = models.TextField(default='', null=True, blank=True)
    tags = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    
    #  Interactions #TODO 
    saved = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="text_saved")
    hidden = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="text_hidden")
    flag = models.ManyToManyField(Flag, blank=True, related_name="text_flag")
    suspended = models.BooleanField(default=False)

    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="text_upvoted")
    downvote= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="text_downvoted")
    # HOW TO ADD COMMENT FLAGS DIRECTLY TO SCRIPT????!? TODO
    
    translations = models.ManyToManyField(Translation, blank=True, related_name="textelements")
    markups = models.ManyToManyField(TextMarkup, blank=True, related_name="textelements")
    #  rating = models.ManyToManyField(Rating, null=True)
    #  comment = models.ManyToManyField(Comment, null=True)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=TextElement)
def add_slug_to_textelement(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.title)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string






# class WebElement(models.Model):
# class DocumentElement(models.Model):





