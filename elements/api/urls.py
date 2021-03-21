from django.urls import path, include, re_path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from elements.api.views import (
    ElementList,
    ElementCommentList,
    CommentReplyList,
    ElementViewSet,
    ElementCommentViewSet,
    CommentReplyViewSet,
    get_element,
    element_togglevote,
    element_togglesave,
    element_togglehide,
    youtube_check,

    youtube_togglesaved,
    youtube_togglehidden,
    YouTubeViewSet,
    youtube_togglevote,
    video_togglesaved,

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

    saved_element_list,

    # get_user_token_view,
    )   

app_name = 'elements'


element_router = DefaultRouter()
element_router.register(r"elementz", ElementViewSet)

element_comment_router = DefaultRouter()
element_comment_router.register(r"elementcommentz", ElementCommentViewSet)

comment_reply_router = DefaultRouter()
comment_reply_router.register(r"commentreplyz", CommentReplyViewSet)



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
    path("", include(element_router.urls)),
    path("", include(element_comment_router.urls)),
    path("", include(comment_reply_router.urls)),
    
    re_path('^list/$', ElementList.as_view(), name="element_list"),
    re_path('^comments/list/$', ElementCommentList.as_view(), name="element_comment_list"),
    re_path('^commentreplies/list/$', CommentReplyList.as_view(), name="comment_reply_list"),
    
    path('element/<slug:slug>/', get_element, name="get_element"),
    path('vote/element/', element_togglevote, name="element_togglevote"),
    path('save/element/', element_togglesave, name="element_togglesave"),
    path('hide/element/', element_togglehide, name="element_togglehide"),
    path('youtube/save/', video_togglesaved, name="video_togglesaved"),
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
    
    path('saved/', saved_element_list, name="saved_element_list"),
]
