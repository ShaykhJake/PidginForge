from django.urls import include, path
# from rest_framework.routers import DefaultRouter
from categories.api import views as cats
from categories.api.views import get_languages

urlpatterns = [
    path('languages/', cats.ListLanguages.as_view(), name="list_languages"),
    path('topics/', cats.ListTopics.as_view(), name="list_topics"),
    path('languages_full/', get_languages, name="get_languges"),

]
