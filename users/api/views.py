import io
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, action

from users.api.serializers import (
                            UserDisplaySerializer, 
                            ProfileSerializer, 
                            CheckEmailAvailableSerializer, 
                            RegistrationSerializer, 
                            CheckUsernameAvailableSerializer, 
                            UserCheckPassSerializer, 
                            ProfileImageSerializer,
                            UpdateProfileSerializer,
                            ProfileListSerializer,
                            )
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.models import Profile, CustomUser



# USER PROFILE LIST
@api_view(['GET',])
def user_profile_list(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            profiles = Profile.objects.all()
            serializer = ProfileListSerializer(profiles, many=True)
            return Response(serializer.data)


# NEW USER
@api_view(['POST',])
def register_user_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = account.email
            data['response'] = account.username
        else:
            data = serializer.errors
            # data = serializer.data
        return Response(data)

# DELETE USER
# TODO
@api_view(['DELETE',])
def delete_user_view(request):
    if request.method == 'DELETE':
        # TODO ENSURE USER HAS PERMISSIONS
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = account.email
            data['response'] = account.username
        else:
            data = serializer.errors
            # data = serializer.data
        return Response(data)


# Check a user's password to confirm it is accurate
@api_view(['POST',])
def check_email_available(request):
    if request.method == 'POST':
        serializer = CheckEmailAvailableSerializer(data=request.data)
        # user = CustomUser.objects.get(pk=request.user.pk)
        # serializer = UserCheckPassSerializer(user)
        data = {}
        if serializer.is_valid():
            if serializer.check_email(request):
                data['response'] = "Indeed, it's available"
                data['available'] = True
            else:
                data['response'] = "Nope, not a chance"
                data['available'] = False
            return Response(data)

@api_view(['POST',])
def change_email(request):
    if request.method == 'POST':
        serializer = CheckEmailAvailableSerializer(data=request.data)
        # user = CustomUser.objects.get(pk=request.user.pk)
        # serializer = UserCheckPassSerializer(user)
        data = {}
        if serializer.is_valid():
            if serializer.change_email(request):
                data['message'] = "Email change initiated! We've sent a test email to the new address. After you confirm the email, the change will be completed."
                data['success'] = True
            else:
                data['message'] = "Email Change Failed"
                data['success'] = False
            return Response(data)

@api_view(['GET',])
def get_snippet(request, username):
    resdata = {}
    if request.method == 'GET':
        if request.user.is_authenticated:
            profile = get_object_or_404(Profile, user__username=username)
            resdata['avatar'] = profile.avatar.url
            resdata['image'] = profile.image.url
            resdata['username'] = profile.user.username
            resdata['language'] = profile.nativelanguage.name
            resdata['biography'] = profile.biography
            resdata['points'] = profile.points
            resdata['followers_count'] = profile.followed.count()
            resdata['user_has_followed'] = profile.followed.filter(pk=request.user.pk).exists()
            resdata['user_has_hidden'] = profile.hidden.filter(pk=request.user.pk).exists()
        else:
            resdata['message'] = 'You must be logged in and authenticated to view profiles'
            resdata['success'] = False
    else:
        resdata['message'] = 'Unknown Failure'
        resdata['success'] = False
    return Response(resdata)


@api_view(['POST'])
def user_togglefollow(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         profile = get_object_or_404(Profile, user__username=(request.data['username']))
         if request.user in profile.followed.all():
            profile.followed.remove(request.user)
            profile.save()
            resdata['message'] = "You are no longer following " + request.data['username']
            resdata['success'] = True
         else: 
            profile.followed.add(request.user)
            profile.save()
            resdata['message'] = "You are now following " + request.data['username']
            resdata['success'] = True
   return Response(resdata)

@api_view(['POST'])
def user_togglehide(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         element = get_object_or_404(Profile, user__username=(request.data['username']))
         if request.user in element.hidden.all():
            element.hidden.remove(request.user)
            element.save()
            resdata['message'] = "Successfully removed " + request.data['username'] + " from your hidden list"
            resdata['success'] = True
         else: 
            element.hidden.add(request.user)
            element.save()
            resdata['message'] = "Successfully added " + request.data['username'] + " to your hidden list"
            resdata['success'] = True
   return Response(resdata)


@api_view(['POST',])
def check_username_available(request):
    if request.method == 'POST':
        serializer = CheckUsernameAvailableSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            if serializer.check_username(request):
                data['message'] = "That username is available!"
                data['success'] = True
                return Response(data)
            else:
                data['message'] = "That username is not available!"
                data['success'] = False
                return Response(data)
        data['message'] = "That username is not available!"
        data['success'] = False
        return Response(data)

@api_view(['POST',])
def change_username(request):
    if request.method == 'POST':
        serializer = CheckUsernameAvailableSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            if serializer.change_username(request):
                data['message'] = "Your username was changed!"
                data['success'] = True
                return Response(data)
            else:
                data['message'] = "That username is not available!"
                data['success'] = False
                return Response(data)
        data['message'] = "There was a problem with your request!"
        data['success'] = False
        return Response(data)


@api_view(['PATCH',])
def update_user_profile(request):
    if request.method == 'PATCH':
        serializer = UpdateProfileSerializer(data=request.data)
        responsedata = {}
        if serializer.is_valid():
            if serializer.updateprofile(request.user, serializer.validated_data):            
                responsedata['message'] = "Your profile was successfully updated!"
                responsedata['success'] = True
                return Response(responsedata)
            else:
                responsedata['message'] = "There was an error with your request!"
                data['success'] = False
                return Response(responsedata)
        responsedata['message'] = "There was a problem with your request!"
        responsedata['success'] = False
        return Response(responsedata)



@api_view(['POST',])
def check_current_password(request):
    if request.method == 'POST':
        serializer = UserCheckPassSerializer(data=request.data)
        # user = CustomUser.objects.get(pk=request.user.pk)
        # serializer = UserCheckPassSerializer(user)
        if serializer.is_valid():
            if serializer.check_password(request):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_409_CONFLICT)

# TODO 
@api_view(['GET','PUT',])
def get_user_profile(request):
    try:
        # user = CustomUser.objects.get(pk=request.user.pk)
        profile = Profile.objects.get(user=request.user.pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


# BASIC PROFILE LIST (For generic view)
# TODO, But not immediate since i have Django Admin
@api_view(['GET','PUT',])
def profile_list_view(request, username):
    try:
        user = CustomUser.objects.get(username=username)
        profile = Profile.objects.get(user=user.pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            profile.save()
            data["success"] = "update successful"
            return Response(data=data)

        return Response("failed")



@api_view(['GET', 'POST',])
def profile_image_update(request):
    if request.method == 'GET':
        serializer = ProfileImageSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            return Response(data)
        return Response(data)

    if request.method == 'POST':
        serializer = ProfileImageSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            if serializer.upload_image(request):
                data['message'] = "Your image has been changed!"
                data['success'] = True
                return Response(data)
            else:
                data['message'] = "There was a problem with your photo!"
                data['success'] = False
                return Response(data)
        data['message'] = "There was a problem with your request!"
        data['success'] = False
        return Response(data)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, )

    def patch(self, request, format=None):
        serializer = ProfileImageSerializer(request.user, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            if serializer.image_update(request):
                # print("Photo successfully changed!")
                data['message'] = "Photo successfully changed!"
                data['success'] = True
            else:
                # print("Damnit! Something broke")
                data['message'] = "There was a problem with your request!"
                data['success'] = False
        return Response(data)
