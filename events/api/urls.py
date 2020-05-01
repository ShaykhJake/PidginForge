from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from events.api.views import (
    CalendarEventViewSet,
    # markup_togglepublish,
    # markup_togglevote,
    # markup_fork,

    # get_user_token_view,
    )   

app_name = 'events'

calendar_event_router = DefaultRouter()
calendar_event_router.register(r"eventz", CalendarEventViewSet)


urlpatterns = [
    path("", include(calendar_event_router.urls)),
    # path('youtube/save/', youtube_togglesaved, name="youtube_togglesaved"),
    # path('youtube/hide/', youtube_togglehidden, name="youtube_togglehidden"),
    # path('youtube/check/', youtube_check, name="youtube_check"),
    # path('youtube/vote/', youtube_togglevote, name="youtube_togglevote"),
        
]
