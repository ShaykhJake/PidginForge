from rest_framework import serializers
from questions.models import Answer, Question, Reply
from users.models import Profile, CustomUser
from categories.models import Language, TopicTag
from categories.api.serializers import LanguageSerializer, TopicTagSerializer, MethodTagSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']

class AuthorSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'user_profile']

class ReplySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    user_has_flagged = serializers.SerializerMethodField()

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        return instance.flag.all().filter(flagger=request.user).exists()

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, at %H:%M")

    class Meta:
        model = Reply
        exclude = ["answer", "flag", "suspended"]

class AnswerSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    # author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    user_has_flagged = serializers.SerializerMethodField()


    class Meta:
        model = Answer
        exclude = ["question","voters","updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, at %H:%M")

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_question_slug(self, instance):
        return instance.question.slug

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


class QuestionSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    # author = serializers.StringRelatedField(read_only=True)
    nativelanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )
    learninglanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )
    topic = serializers.SlugRelatedField(
        queryset = TopicTag.objects.all(),
        read_only=False,
        slug_field='name'
    )

    tags = serializers.ListField(child=serializers.CharField(max_length=50))
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    answers_count = serializers.SerializerMethodField()
    user_has_answered = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()
    user_has_saved = serializers.SerializerMethodField()
    filtered = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    user_has_flagged = serializers.SerializerMethodField()

    def get_filtered(self, instance):
        request = self.context.get("request")
        # if instance.hidden.filter(pk=request.user.pk).exists():
        #     return True
        if instance.nativelanguage not in request.user.user_profile.learninglanguage.all():
            return True
        if instance.learninglanguage not in request.user.user_profile.learninglanguage.all():
            return True
        elif instance.topic not in request.user.user_profile.learningtopics.all():
            return True
        else:
            return False

    class Meta:
        model = Question
        exclude = ["updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, at %H:%M")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()

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
