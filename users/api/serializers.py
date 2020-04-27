from rest_framework import serializers
from users.models import CustomUser, Profile
from categories.models import Language, TopicTag
from categories.api.serializers import LanguageSerializer, TopicTagSerializer, MethodTagSerializer

import boto3
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # bob = Profile.objects.filter(user=model)
        fields = ['username','email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)


    image_name = serializers.SerializerMethodField(read_only=True)
    # user = Profile.CustomUser.username
    biography = serializers.CharField(max_length=600, min_length=None, allow_blank=True)
    country = serializers.CharField(max_length=100, min_length=None, allow_blank=True)
    image = serializers.ImageField(max_length=150, allow_empty_file=False)
    avatar = serializers.ImageField(max_length=150, allow_empty_file=False)
    # nativelanguage = LanguageSerializer()
    
    nativelanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    learninglanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        many=True,
        read_only=False,
        slug_field='name'
    )
    # learninglanguage = LanguageSerializer(many=True)

    # learningtopics = TopicTagSerializer(many=True)
    learningtopics = serializers.SlugRelatedField(
        queryset = TopicTag.objects.all(),
        many=True,
        read_only=False,
        slug_field='name'
    )

    points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'biography', 'country', 'image', 'avatar', 'nativelanguage', 'learninglanguage', 'learningtopics', 'points', 'image_name']
    
    def get_user(self, instance, request):
        return instance.voters.count()
    
    def get_image_name(self, profile):
        request = self.context.get('request')
        image_name = profile.image.name.split("/")[-1]
        return image_name

class UpdateProfileSerializer(serializers.ModelSerializer):
    nativelanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    learninglanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        many=True,
        read_only=False,
        slug_field='name'
    )

    learningtopics = serializers.SlugRelatedField(
        queryset = TopicTag.objects.all(),
        many=True,
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = Profile
        fields = ['nativelanguage', 'learninglanguage', 'learningtopics', 'biography']

    def updateprofile(self, user, profiledata):
        profile = Profile.objects.get(user = user.pk)
        profile.nativelanguage = profiledata['nativelanguage']
        profile.learninglanguage.set(profiledata['learninglanguage'])
        profile.learningtopics.set(profiledata['learningtopics'])
        profile.biography = profiledata['biography']
        print("HELLO!")
        profile.save()
        # profile.save(update_fields=['nativelanguage', 'learninglanguage', 'learningtopics', 'biography'])
        return True
    


# This will be used for updating a user's profile (Image & Avatar are separate)
class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)

    # user = Profile.CustomUser.username
    biography = serializers.CharField(max_length=600, min_length=None, allow_blank=True)
    country = serializers.CharField(max_length=100, min_length=None, allow_blank=True)
    nativelanguage = LanguageSerializer()
    learninglanguage = LanguageSerializer(many=True)
    learningtopics = TopicTagSerializer(many=True)
    # points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'biography', 'country', 'nativelanguage', 'learninglanguage', 'learningtopics', 'points',]


# Image & Avatar Updating
# This serializer checks the incoming file from CopperJS, then resizes it to below 300x300, then autogenerates an Avatar to go with it.
class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=150, allow_empty_file=False)

    class Meta:
        model = Profile
        fields = ['image',]
        
    def image_update(self, request):
        print("Starting update")
        newimage = self.validated_data['image']
        newimagename = newimage.name

        profile = Profile.objects.get(user = request.user.pk)
        data = {}

        # if profile.image.name:
        #     old_image_name = profile.image.name
        #     if old_image_name != "profile_pics/default.jpg":
        #         profile.image.storage.delete(old_image_name)

        profile.image = newimage
        profile.save()

        imageTemporary = Image.open(profile.image.storage.open(profile.image.name))
        outputIoStream = BytesIO()

        #set profile photo max size preferences (these are max for both)
        basewidth = 300
        baseheight = 300
        if float(imageTemporary.size[0]) > basewidth or float(imageTemporary.size[1]) > baseheight:
            if float(imageTemporary.size[0]) > float(imageTemporary.size[1]):
                wpercent = (basewidth/float(imageTemporary.size[0]))
                hsize = int((float(imageTemporary.size[1])*float(wpercent)))
                wsize = basewidth
            else:
                hpercent = (baseheight/float(imageTemporary.size[1]))
                wsize = int((float(imageTemporary.size[0])*float(hpercent)))
                hsize = baseheight
            imageTemporaryResized = imageTemporary.resize((wsize,hsize), Image.ANTIALIAS ) 
            imageTemporaryResized.save(outputIoStream , format='JPEG', quality=85)
            outputIoStream.seek(0)
            profile.image.storage.delete(profile.image.name)
            profile.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %newimagename.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
            profile.save()
        imageTemporary.close()
        
        # Create Avatar:
        avatarTemporary = Image.open(profile.image.storage.open(profile.image.name)) 
        outputIoStream = BytesIO()
        #set avatar photo max size preferences (these are max for both)
        basewidth = 175
        baseheight = 175
        if float(avatarTemporary.size[0]) > basewidth or float(avatarTemporary.size[1]) > baseheight:
            print("Smushing avatar")
            if float(avatarTemporary.size[0]) > float(avatarTemporary.size[1]):
                wpercent = (basewidth/float(avatarTemporary.size[0]))
                hsize = int((float(avatarTemporary.size[1])*float(wpercent)))
                wsize = basewidth
            else:
                hpercent = (baseheight/float(avatarTemporary.size[1]))
                wsize = int((float(avatarTemporary.size[0])*float(hpercent)))
                hsize = baseheight
            avatarTemporary = avatarTemporary.resize((wsize,hsize), Image.ANTIALIAS ) 
        avatarTemporary.save(outputIoStream, format='JPEG', quality=80)
        outputIoStream.seek(0)
        # if profile.avatar and profile.avatar.name != "avatars/default.jpg":
        #     profile.avatar.storage.delete(profile.avatar.name)
        profile.avatar = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %newimagename.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        profile.save()
        avatarTemporary.close()

        return True

class UserCheckPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def check_password(self, request):
        password = self.validated_data['password']
        if request.user.check_password(password):
            return True
        else:
            return False

class CheckEmailAvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

    def check_email(self, request):
        email = self.validated_data['email']
        num_results = CustomUser.objects.filter(email = email).count()

        if num_results == 0:
            return True
        else:
            return False

    def change_email(self, request):
        new_email = self.validated_data['email']
        num_results = CustomUser.objects.filter(email = new_email).count()
        if num_results == 0:
            user = CustomUser.objects.get(pk = request.user.pk)
            # new_email = request.POST.get('new_email')
            user.add_email_address(request, new_email)
            # user = CustomUser.objects.get(pk = request.user.pk)
            # user.email = email
            # print(user.email)
            # user.save()
            # user = CustomUser.objects.get(pk = request.user.pk)
            # print(user.email)
            return True
        else:
            return False

class CheckUsernameAvailableSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username']
        
        # extra_kwargs = {
        #     'username': {'write_only': True}
        # }

    def check_username(self, request):
        username = self.validated_data['username']
        if username.lower() == request.user.username.lower():
            return True
        else:
            num_results = CustomUser.objects.filter(username__iexact = username).count()
            if num_results == 0:
                return True
        return False

    def change_username(self, request):
        username = self.validated_data['username']
        if username.lower() == request.user.username.lower():
            user = CustomUser.objects.get(pk = request.user.pk)
            # new_email = request.POST.get('new_email')
            user.username = username
            user.save()
            return True
        else:
            num_results = CustomUser.objects.filter(username__iexact = username).count()
            if num_results == 0:
                user = CustomUser.objects.get(pk = request.user.pk)
                user.username = username
                user.save()
                return True
        return False
        


class UserSerializer(serializers.ModelSerializer):
    newuser = ProfileSerializer()

    class Meta:
        model = CustomUser
        # bob = Profile.objects.filter(user=model)
        fields = ['username','userProfile']

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)

        instance.save()
        return instance
        

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match!'})

        account.set_password(password)
        account.save()
        return account
