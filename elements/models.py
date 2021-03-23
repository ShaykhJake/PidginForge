from django.db import models
from django.urls import reverse
from django.conf import settings
from model_utils.managers import InheritanceManager
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


ELEMENT_CHOICES = (
    ("Text", "Text"),
    ("Audio", "Audio"),
    ("YouTube", "YouTube"),
)

class Element(models.Model):
    # https://django-model-utils.readthedocs.io/en/latest/managers.html#inheritancemanager
    objects = InheritanceManager()

    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="element_curator")
    curation_date = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=150, default="", null=False)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True, null=True, blank=True)

    # Categories
    description = models.CharField(max_length=300, default="", null=False, db_index=True)
    citation = models.CharField(max_length=300, default="", null=False)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    tags = ArrayField(models.CharField(max_length=25), blank=True, null=True)
    sub_type = models.CharField(max_length=20, choices=ELEMENT_CHOICES, default="text")
    flag = models.ManyToManyField(Flag, blank=True, related_name="elements")
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sub_type} { self.title }"
    
    def short(self):
        return self.description[:75] + '...'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.title[:50]
            slug = slugify(value, allow_unicode=True)
            random_string = generate_random_string()
            self.slug = slug + "-" + random_string
        super().save(*args, **kwargs)

class Text(Element):
    rich_text = JSONField(blank=True, default=dict)
    plain_text = models.TextField(default='', db_index=True)
    thumb = models.ImageField(default='elements/default_text.jpg', upload_to='elements/%Y/%m/%d')

class YouTube(Element):
    duration = models.PositiveIntegerField(default=0)
    video_id = models.CharField(max_length=100)
    thumb = models.CharField(max_length=200)

class Audio(Element):
    duration = models.PositiveIntegerField(default=0)
    audiofile = models.FileField(upload_to='audio_files/%Y/%m/%d')
    originalfilename = models.CharField(max_length=200, default="", null=False)
    thumb = models.ImageField(default='elements/default_audio.jpg', upload_to='elements/%Y/%m/%d')

class ElementUpVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="element_upvotes")
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="upvotes")

class ElementDownVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="element_downvotes")
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="downvotes")

class ElementSave(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="element_saves")
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="saves")

class ElementHide(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="element_hides")
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="hides")

class ElementComment(models.Model):
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="element_comments")
    curation_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    rich_text = JSONField(blank=True, default=dict)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="comments")
    plain_text = models.TextField(default='')
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.curator.username} - {self.plain_text[0:30]}"

class CommentReply(models.Model):
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="element_comment_replies")
    curation_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    rich_text = JSONField(blank=True, default=dict)
    plain_text = models.TextField(default='')
    comment = models.ForeignKey(ElementComment, on_delete=models.CASCADE, related_name="replies")
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.curator.username} - {self.plain_text[:30]}"


class Translation(models.Model):
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="translation_curator") #do we want this to be null?
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    curation_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    rich_text = JSONField(null=True, blank=True)
    plain_text = models.TextField(default='', db_index=True)
    notes = models.TextField(default='', null=True, blank=True)
    published = models.BooleanField(default=False)
    forkparent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='forks')
    
    def __str__(self):
        if (self.curator and self.targetlanguage):
            return self.curator.username + " on " + self.curationdate.strftime("%B %d, %Y") + " in " + self.targetlanguage.name 
        else:
            return "Object Orphaned"


class Transcript(models.Model):
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="transcript_curator") #do we want this to be null?
    curation_date = models.DateTimeField(auto_now_add=True, editable=False)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=True, related_name="transcripts")
    updated = models.DateField(auto_now=True, editable=False)
    rich_text = JSONField(null=True, blank=True)
    plain_text = models.TextField(default='', db_index=True)
    notes = models.TextField(default='', null=True, blank=True)
    published = models.BooleanField(default=False)
    forkparent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='forks')

    def __str__(self):
        if (self.curator):
            return self.curator.username + " on " + self.curation_date.strftime("%B %d, %Y")
        return "Object Orphaned"

# class ElementTranscript:
#     created = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="element_saves")


#     curator
#     curation_date
#     language
#     updated
#     content (should this be json???)

#     pass


"""

class Reply(models.Model):
    pass 

class MediaComment(models.Model): TODO should this be for the Media or the note?
    simple text field (non-json)
    pass



class MediaTranslation:
    pass


class 
"""




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
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True, null=True, blank=True)

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
        slug = slugify(instance.title, allow_unicode=True)
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
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True, null=True, blank=True)

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
        slug = slugify(instance.title, allow_unicode=True)
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
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True, null=True, blank=True)

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
        slug = slugify(instance.title, allow_unicode=True)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string


# class WebElement(models.Model):
# class DocumentElement(models.Model):

class SavedVideo(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   youtube_element = models.ForeignKey(YouTubeElement, on_delete=models.CASCADE)

class SavedAudio(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   audio_element = models.ForeignKey(AudioElement, on_delete=models.CASCADE)

class SavedText(models.Model):
   curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   text_element = models.ForeignKey(TextElement, on_delete=models.CASCADE)



