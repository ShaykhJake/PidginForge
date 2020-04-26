from django.urls import path, include
from users.api.views import (
    register_user_view,
    # check_current_password,
    check_username_available,
    change_username,
    get_user_profile,
    check_email_available,
    update_user_profile,
    change_email,
    change_image,
    FileUploadView,
    get_snippet,
    user_togglefollow,
    user_togglehide,
    # get_user_token_view,
    )   
from rest_framework.authtoken import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('', ChangeProfileImage, 'images')

# from rest_framework.routers import DefaultRouter

app_name = 'users'

urlpatterns = [
    path('register/', register_user_view, name="register"),
    path('gettoken/', views.obtain_auth_token),
    path('checkemail/', check_email_available, name="checkemail"),
    path('changeemail/', change_email, name="changeemail"),
    path('checkusername/', check_username_available, name="checkusername"),
    path('changeusername/', change_username, name="changeusername"),
    path('profile/update/', update_user_profile, name="updateprofile"),
    path('profile/', get_user_profile, name="getprofile"),
    path('follow/', user_togglefollow, name="user_togglefollow"),
    path('hide/', user_togglehide, name="user_togglehide"),

    path('snippet/<str:username>', get_snippet, name="get_snippet"),
    # path('profileimageupdate/', profile_image_update, name="profileimageupdate"),
    # path('profileimage/', include(router.urls)),
    path('profileimageupload/', FileUploadView.as_view(), name="imageupload"),
    # path('profileimageupload/', change_image, name="imageupload"),
    # path('profile/<str:username>/', api_detail_profile_view, name="detail"),
    # path('profile/<str:username>/update/', api_detail_profile_view, name="detail"),
    # path('profile/<str:username>/delete/', api_detail_profile_view, name="delete"),
]

## NOTE: The following URLs are for REST AUTH:
# API endpoints

# DONE Logout:
# /rest-auth/logout/ (POST)

# Now TODO: Change Password
# /rest-auth/password/change/ (POST)
# old_password
# new_password1
# new_password2
# Note: OLD_PASSWORD_FIELD_ENABLED = True to use old_password.
# Note: LOGOUT_ON_PASSWORD_CHANGE = False to keep the user logged in after password change

# Now TODO: User Account Update: 
# /rest-auth/user/ (GET, PUT, PATCH)
# username
# first_name
# last_name
# Returns pk, username, email, first_name, last_name


# nearterm TODO: Basic Login:  (This will be necessary if we have an anonymous view)
# /rest-auth/login/ (POST)
# username
# email
# password
# (Returns Token key)

# N/A
# Confirm email:

# N/A
# Password Reset:
# /rest-auth/password/reset/confirm/ (POST)
# uid
# token
# new_password1
# new_password2
# Note: uid and token are sent in email after calling /rest-auth/password/reset/


# Currently N/A: User Registration (This currently requires a token; it might be a TODO at some point...)
# /rest-auth/registration/ (POST)
# username
# password1
# password2
# email

# Currently N/A: User Email Verify
# /rest-auth/registration/verify-email/ (POST)
# key
