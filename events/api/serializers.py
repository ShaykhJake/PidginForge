from rest_framework import serializers
from users.models import CustomUser, Profile
from events.models import (
                     CalendarEvent,
                     EventRSVP, 
                     EventAttendee, 
                     EventComment, 
                     CommentReply,
                     )
from categories.models import Language
from categories.api.serializers import LanguageSerializer, MethodTagSerializer
from rest_framework.generics import get_object_or_404

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']

class UserSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)
    slug_field='username'

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_profile']


class RSVPSerializer(serializers.ModelSerializer):
    # invited_user = serializers.SlugRelatedField(
    #     # queryset = CustomUser.objects.all(),
    #     read_only = True,
    #     slug_field ='username'
    # )
    invited_user = UserSerializer()
    class Meta:
        model = EventRSVP
        fields = '__all__'




class CalendarEventSerializer(serializers.ModelSerializer):
    curator = UserSerializer(read_only=True)

    rsvp_list_count = serializers.SerializerMethodField()
    rsvp_list = serializers.SerializerMethodField()
    user_rsvp = serializers.SerializerMethodField()
    
    # guest_list = serializers.SerializerMethodField()
    # rsvp_list = serializers.SerializerMethodField()

    guest_list = serializers.SlugRelatedField(
        queryset = CustomUser.objects.all(),
        many=True,
        read_only=False,
        slug_field='username'
    )

    native_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    target_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = CalendarEvent
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_rsvp_list_count(self, instance):
        return instance.rsvp.count()
    
    def get_rsvp_list(self, instance):
        request = self.context.get("request")
        # rsvps = instance.rsvp.all()
        serializer = RSVPSerializer(instance.rsvp, context={'request': request}, many=True)
        return serializer.data

    def get_user_rsvp(self, instance):
        request = self.context.get("request")
        user_rsvp = instance.rsvp.filter(invited_user=request.user)
        if user_rsvp:
            serializer = RSVPSerializer(user_rsvp[0], context={'request': request})
            return serializer.data
        else:
            return False

