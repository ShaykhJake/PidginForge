from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from elements.api.views import (
    youtube_check,
    youtube_togglesaved,
    youtube_togglehidden,
    YouTubeViewSet,
    youtube_togglevote,

    AudioViewSet,
    audio_togglesaved,
    audio_togglehidden,
    audio_togglevote,

    TextViewSet,
    text_togglesaved,
    text_togglehidden,
    text_togglevote,
    # audio_check,

    TranscriptViewSet,
    transcript_togglepublish,
    transcript_togglevote,

    TranslationViewSet,
    translation_togglepublish,
    translation_togglevote,

    MarkupViewSet,
    markup_togglepublish,
    markup_togglevote,
    markup_fork,

    # get_user_token_view,
    )   

app_name = 'elements'

youtube_router = DefaultRouter()
youtube_router.register(r"youtubez", YouTubeViewSet)

audio_router = DefaultRouter()
audio_router.register(r"audioz", AudioViewSet)

transcript_router = DefaultRouter()
transcript_router.register(r"transcriptz", TranscriptViewSet)

text_router = DefaultRouter()
text_router.register(r"textz", TextViewSet)

translation_router = DefaultRouter()
translation_router.register(r"translationz", TranslationViewSet)

markup_router = DefaultRouter()
markup_router.register(r"markupz", MarkupViewSet)


urlpatterns = [
    path("", include(youtube_router.urls)),
    path('youtube/save/', youtube_togglesaved, name="youtube_togglesaved"),
    path('youtube/hide/', youtube_togglehidden, name="youtube_togglehidden"),
    path('youtube/check/', youtube_check, name="youtube_check"),
    path('youtube/vote/', youtube_togglevote, name="youtube_togglevote"),
    
    path("", include(audio_router.urls)),
    path('audio/save/', audio_togglesaved, name="audio_togglesaved"),
    path('audio/hide/', audio_togglehidden, name="audio_togglehidden"),
    path('audio/vote/', audio_togglevote, name="audio_togglevote"),

    path("", include(text_router.urls)),
    path('text/save/', text_togglesaved, name="text_togglesaved"),
    path('text/hide/', text_togglehidden, name="text_togglehidden"),
    path('text/vote/', text_togglevote, name="text_togglevote"),

    path("", include(transcript_router.urls)),
    path('transcript/publish/', transcript_togglepublish, name="transcript_togglepublish"),
    path('transcript/vote/', transcript_togglevote, name="transcript_togglevote"),

    path("", include(translation_router.urls)),
    path('translation/publish/', translation_togglepublish, name="translation_togglepublish"),
    path('translation/vote/', translation_togglevote, name="translation_togglevote"),

    path("", include(markup_router.urls)),
    path('markup/publish/', markup_togglepublish, name="markup_togglepublish"),
    path('markup/vote/', markup_togglevote, name="markup_togglevote"),
    path('markup/fork/', markup_fork, name="markup_fork"),
    
]
