from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from lessons.api.views import (
    LessonViewSet,
    lesson_togglesaved,
    lesson_togglehidden,
    lesson_togglevote,
    create_lesson_vocab,

    )   

app_name = 'lessons'

lesson_router = DefaultRouter()
lesson_router.register(r"lessonz", LessonViewSet)


urlpatterns = [
    path('save/', lesson_togglesaved, name="lesson_togglesaved"),
    path('hide/', lesson_togglehidden, name="lesson_togglehidden"),
    path('vote/', lesson_togglevote, name="lesson_togglevote"),
    path('createvocab/', create_lesson_vocab, name="create_lesson_vocab"),
    path("", include(lesson_router.urls)),
]
