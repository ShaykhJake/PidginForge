from django.urls import path, include
from rest_framework.authtoken import views
from malapropos.api.views import (
    flag_item,
    # review_flag
    )   

app_name = 'malapropos'

urlpatterns = [
    path('flag/', flag_item, name="flag_item"),
    # path('review/<int:pk>/', review_flag, name="review_flag"),
]
