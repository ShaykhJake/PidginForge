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
    # audio_check,

    TranscriptViewSet,
    transcript_togglepublish,
    transcript_togglevote,

    TranslationViewSet,
    translation_togglepublish,
    translation_togglevote

    # get_user_token_view,
    )   

app_name = 'elements'

youtube_router = DefaultRouter()
youtube_router.register(r"youtubez", YouTubeViewSet)

audio_router = DefaultRouter()
audio_router.register(r"audioz", AudioViewSet)

transcript_router = DefaultRouter()
transcript_router.register(r"transcriptz", TranscriptViewSet)

translation_router = DefaultRouter()
translation_router.register(r"translationz", TranslationViewSet)


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
    
    path("", include(transcript_router.urls)),
    path('transcript/publish/', transcript_togglepublish, name="transcript_togglepublish"),
    path('transcript/vote/', transcript_togglevote, name="transcript_togglevote"),

    path("", include(translation_router.urls)),
    path('translation/publish/', translation_togglepublish, name="translation_togglepublish"),
    path('translation/vote/', translation_togglevote, name="translation_togglevote")
]
