import serpy

from rest_framework import serializers
from users.models import CustomUser, Profile
from lessons.models import (
                     Lesson,
                     LessonVocabBank,
                     SavedLesson,
                     )
from categories.models import Language
from categories.api.serializers import LanguageSerializer, MethodTagSerializer
from vocab.api.serializers import InflectedFormPairSerializer
from rest_framework.generics import get_object_or_404


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']
        read_only_fields = fields

class UserSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)
    slug_field='username'

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_profile']
        read_only_fields = fields


class CuratorSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)
    slug_field='username'

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_profile']
        read_only_fields = fields
 
class LessonVocabBankSerializer(serializers.ModelSerializer):
    curator = UserSerializer(read_only=True)
    curation_date = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    word_pairs = InflectedFormPairSerializer(many=True, read_only=True)

    class Meta:
        model = LessonVocabBank
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curation_date', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")
    
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

    curation_date = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()
    # user_has_saved = serializers.SerializerMethodField()
    # user_has_hidden = serializers.SerializerMethodField()
    # user_vote = serializers.SerializerMethodField()
    # upvote_count = serializers.SerializerMethodField()
    # downvote_count = serializers.SerializerMethodField()
    # flag_count = serializers.SerializerMethodField()
    # user_has_flagged = serializers.SerializerMethodField()
    vocab_banks = serializers.SerializerMethodField()    
    tags = serializers.ListField(child=serializers.CharField(max_length=50), allow_empty=True, required=False)

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")

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
        return instance.saves.count()

    def get_user_has_saved(self, instance):
        request = self.context.get("request")
        return instance.saves.filter(user=request.user).exists()

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return instance.hides.filter(user=request.user).exists()

    def get_vocab_banks(self, instance):
        vocab_banks = instance.lessonvocabbank_set
        return LessonVocabBankSerializer(vocab_banks, many=True).data


class QuickLessonSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    source_language = serializers.SerializerMethodField()
    curation_date = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)

    class Meta:
        model = Lesson
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag']

    # This currently is only allowing published transcripts
    def get_source_language(self, instance):
        return instance.source_language.name

    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedlesson_set.count()

    
class LessonListSerializer(serializers.ModelSerializer):
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

    curation_date = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()
    user_has_saved = serializers.SerializerMethodField()
    # upvote_count = serializers.SerializerMethodField()
    # downvote_count = serializers.SerializerMethodField()

    # user_has_hidden = serializers.SerializerMethodField()
    # user_vote = serializers.SerializerMethodField()
    # user_has_flagged = serializers.SerializerMethodField()
    # vocab_banks = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField(max_length=50), allow_empty=True, required=False)

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['title', 'curation_date','saved_count', 'vocab_banks', 'notes', 'tags', 'curator', 'source_language', 'target_language', 'tags', 'saved_count']

    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")

    # def get_user_vote(self, instance):
    #     request = self.context.get("request")
    #     if instance.upvote.filter(pk=request.user.pk).exists():
    #         return 1
    #     elif instance.downvote.filter(pk=request.user.pk).exists():
    #         return -1
    #     else:
    #         return 0

    # def get_flag_count(self, instance):
    #     return instance.flag.count()

    # def get_user_has_flagged(self, instance):
    #     request = self.context.get("request")
    #     return instance.flag.all().filter(flagger=request.user).exists()

    # def get_upvote_count(self, instance):
    #     return instance.upvote.count()

    # def get_downvote_count(self, instance):
    #     return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.saves.count()

    def get_user_has_saved(self, instance):
        request = self.context.get("request")
        return instance.saves.filter(user=request.user).exists()

    # def get_user_has_hidden(self, instance):
    #     request = self.context.get("request")
    #     return instance.hidden.filter(pk=request.user.pk).exists()

    # def get_vocab_banks(self, instance):
    #     vocab_banks = instance.lessonvocabbank_set
    #     return LessonVocabBankSerializer(vocab_banks, many=True).data
