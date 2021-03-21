from django.contrib import admin
from elements.models import (
    Element,
    Text,
    Audio,
    YouTube,
    ElementUpVote,
    ElementDownVote,
    ElementSave,
    ElementHide,
    Transcript,
    Translation,
    YouTubeElement,
    AudioElement,
    TextElement,
    TextMarkup,
    SavedVideo,
    SavedAudio,
    SavedText
)
# Register your models here.

admin.site.register(Element)
admin.site.register(ElementDownVote)
admin.site.register(ElementUpVote)
admin.site.register(ElementSave)
admin.site.register(ElementHide)
admin.site.register(Audio)
admin.site.register(YouTube)
admin.site.register(Text)
admin.site.register(Transcript)
admin.site.register(Translation)
admin.site.register(YouTubeElement)
admin.site.register(AudioElement)
admin.site.register(TextElement)
admin.site.register(TextMarkup)
admin.site.register(SavedVideo)
admin.site.register(SavedAudio)
admin.site.register(SavedText)
