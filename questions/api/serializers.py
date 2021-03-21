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
    # flag_count = serializers.SerializerMethodField()
    # user_has_flagged = serializers.SerializerMethodField()

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
    created_at = serializers.SerializerMethodField()    
    question_slug = serializers.SerializerMethodField()
    # flag_count = serializers.SerializerMethodField()
    # user_has_flagged = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ["question","updated_at"]

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
        if instance.upvotes.filter(user=request.user).exists():
            return 1
        elif instance.downvotes.filter(user=request.user).exists():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvotes.count()

    def get_downvote_count(self, instance):
        return instance.downvotes.count()

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
    tags = serializers.ListField(child=serializers.CharField(max_length=50))
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)

    answers_count = serializers.SerializerMethodField(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True)
    user_has_answered = serializers.SerializerMethodField(read_only=True)

    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    # user_upvote = serializers.BooleanField(read_only=True)
    # user_downvote = serializers.BooleanField(read_only=True)
    # user_vote = serializers.SerializerMethodField(read_only=True)

    saved_count = serializers.SerializerMethodField(read_only=True)
    user_has_saved = serializers.SerializerMethodField(read_only=True)

    # flag_count = serializers.SerializerMethodField()
    # user_has_flagged = serializers.SerializerMethodField()

    def get_filtered(self, instance):
        request = self.context.get("request")
        # if instance.hidden.filter(pk=request.user.pk).exists():
        #     return True
        if instance.nativelanguage not in request.user.user_profile.learninglanguage.all():
            return True
        if instance.learninglanguage not in request.user.user_profile.learninglanguage.all():
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
        return instance.upvotes.count()

    def get_downvote_count(self, instance):
        return instance.downvotes.count()

    def get_user_vote(self, instance):
        if instance.user_upvote:
            return 1
        elif instance.user_downvote:
            return -1
        else:
            return 0

    def get_saved_count(self, instance):
        return instance.saves.count()

    def get_user_has_saved(self, instance):
        request = self.context.get("request")
        return instance.saves.filter(user=request.user).exists()


class QuestionListSerializer(serializers.Serializer):
    author = AuthorSerializer(read_only=True)
    # author = serializers.StringRelatedField(read_only=True)
    nativelanguage = serializers.SerializerMethodField()
    title = serializers.CharField()
    learninglanguage = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField(max_length=50))
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)

    answers_count = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()
    user_has_saved = serializers.BooleanField(read_only=True, required=False)

    def get_nativelanguage(self, instance):
        return instance.nativelanguage.name

    def get_learninglanguage(self, instance):
        return instance.learninglanguage.name
        
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, at %H:%M")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_upvote_count(self, instance):
        return instance.upvotes.count()

    def get_downvote_count(self, instance):
        return instance.downvotes.count()

    def get_saved_count(self, instance):
        return instance.saves.count()
