from django.db import models

# TODO Create your models here.
# class LearningObject(models.Model):
#     # The original curator of the object:
#     curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     # Those granted authority to assist with the object:
#     image = models.ImageField(upload_to='objectimage/%Y/%m/%d', null=True, blank=True)
#     audio = models.FileField(upload_to='objectaudio/%Y/%m/%d', null=True, blank=True)
#     videolink = models.CharField(max_length=200, null=True, blank=True)
#     weblink = models.CharField(max_length=200, null=True, blank=True)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     language = models.ManyToManyField(Language, related_name="language")
#     topictags = models.ManyToManyField(TopicTag)
#     citation = models.TextField()
#     collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="objectcollaborators", blank=True)
#     published = models.BooleanField(default=False)
#     curationdate = models.DateTimeField(auto_now_add=True, editable=False)
#     # comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
#     # TODO need to implement number of views
#     views = models.PositiveIntegerField(null=True, editable=False)
#     # Linked Lessons
#     # Linked Transcripts
#     # Linked Vocabulary
#     # Linked Translations
#     # source_rawtranscript = models.TextField(default='')
#     # target_rawtranslation = models.TextField(default='')
#     # TODO RATINGS: totalratings is number of times rated
#     # TODO Progressions
#     # TODO source_media = models.ForeignKey(MediaObject)

#     def __str__(self):
#         return self.title
    
#     def short(self):
#         return self.description[:250] + '...'

#     def get_absolute_url(self):
#         return reverse("learningobject-detail", kwargs={"pk": self.pk})
    
#     def alltags(self):
#         return ', '.join([a.name for a in self.topictags.all()])
    
#     def alllanguages(self):
#         return ', '.join([a.name for a in self.language.all()])

# class Lesson(models.Model):
#     # The original curator of the lesson:
#     curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

#     # Those granted authority to assist with the object:
#     collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="lessoncollaborators", blank=True)
#     title = models.CharField(max_length=200)
#     nativelanguage = models.ManyToManyField(Language, related_name="native_language")
#     foreignlanguage = models.ManyToManyField(Language, related_name="foreign_language", blank=True)
#     topictags = models.ManyToManyField(TopicTag)
#     methodtags = models.ManyToManyField(MethodTag)
#     coverimage = models.ImageField(upload_to='lessonimage/%Y/%m/%d', null=True, blank=True)
#     lessonoverview = models.TextField(default='', null=True, blank=True)
#     lessoncontent = models.TextField(default='', null=True, blank=True)
#     notes = models.TextField(default='', null=True, blank=True)

#     linkedobjects = models.ManyToManyField(LearningObject, blank=True)
#     # audio = models.FileField(upload_to='objectaudio/%Y/%m/%d', null=True, blank=True)
#     # videolink = models.CharField(max_length=200, null=True, blank=True)
#     # videolink = models.CharField(max_length=200, null=True, blank=True)

#     citation = models.TextField()    
#     published = models.BooleanField(default=False)
#     curationdate = models.DateTimeField(auto_now_add=True, editable=False)
#     updateddate = ...
#     # views = models.PositiveIntegerField(null=True, editable=False)
#     # TODO RATINGS: totalratings is number of times rated
#     # TODO Object QCers: These are the people who have site-wide privileges to QC
#     # object_qcers
#     # totalratings
#     # totalpoints
#     # TODO Accreditation
#     # NEED TO IMPLEMENT SOMETHING THAT CHANGES ACCREDITATION STATUS WHEN CHANGED
#     # TODO Progressions
#     # TODO source_media = models.ForeignKey(MediaObject)
#     # TODO Implement draft/published False = still in draft, True = Published
#     # TODO publication_date
#     # TODO revision_date

#     def __str__(self):
#         return self.title
    
#     def short(self):
#         return self.lessonoverview[:250] + '...'

#     # def get_absolute_url(self):
#     #     return reverse("lesson-detail", kwargs={"pk": self.pk})
    
#     def alltopic(self):
#         return ', '.join([a.name for a in self.topictags.all()])

#     def allmethodtags(self):
#         return ', '.join([a.name for a in self.methodtags.all()])

#     # def alllanguages(self):
#     #     return ', '.join([a.name for a in self.language.all()])
