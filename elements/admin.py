from django.contrib import admin
from elements.models import Transcript, Translation, YouTubeElement, AudioElement
# Register your models here.

admin.site.register(Transcript)
admin.site.register(Translation)
admin.site.register(YouTubeElement)
admin.site.register(AudioElement)