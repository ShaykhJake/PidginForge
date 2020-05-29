from rest_framework import serializers
from users.models import CustomUser, Profile
from lessons.models import (
                     Lesson,
                     LessonVocabBank,
                     )
from categories.models import Language, TopicTag
from categories.api.serializers import LanguageSerializer, TopicTagSerializer, MethodTagSerializer
from vocab.api.serializers import InflectedFormPairSerializer
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


class CuratorSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)
    slug_field='username'

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_profile']
 
class LessonVocabBankSerializer(serializers.ModelSerializer):
    curator = UserSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    word_pairs = InflectedFormPairSerializer(many=True, read_only=True)

    class Meta:
        model = LessonVocabBank
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")




class LessonSerializer(serializers.ModelSerializer):
    curator = UserSerializer(read_only=True)

    source_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    target_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    topic = serializers.SlugRelatedField(
        queryset = TopicTag.objects.all(),
        read_only=False,
        slug_field='name'
    )

    curationdate = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()
    user_has_saved = serializers.SerializerMethodField()
    user_has_hidden = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    user_has_flagged = serializers.SerializerMethodField()
    filtered = serializers.SerializerMethodField()

    vocab_banks = serializers.SerializerMethodField()
    
    notes = serializers.CharField(required=False, max_length=300, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=50), allow_empty=True, required=False)

    class Meta:
        model = Lesson
        # fields = '__all__'
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag']

    def get_filtered(self, instance):
        request = self.context.get("request")
        if instance.hidden.filter(pk=request.user.pk).exists():
            return True
        if instance.source_language != request.user.user_profile.nativelanguage:
            return True
        if instance.target_language not in request.user.user_profile.learninglanguage.all():
            return True
        elif instance.topic not in request.user.user_profile.learningtopics.all():
            return True
        else:
            return False

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        return instance.flag.all().filter(flagger=request.user).exists()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.saved.count()

    def get_user_has_saved(self, instance):
        request = self.context.get("request")
        return instance.saved.filter(pk=request.user.pk).exists()

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return instance.hidden.filter(pk=request.user.pk).exists()

    def get_vocab_banks(self, instance):
        vocab_banks = LessonVocabBank.objects.filter(lesson=instance)
        return LessonVocabBankSerializer(vocab_banks, many=True).data