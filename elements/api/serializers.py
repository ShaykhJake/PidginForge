from rest_framework import serializers
from users.models import CustomUser, Profile
from elements.models import YouTubeElement, AudioElement, Translation, Transcript, TextElement, TextMarkup
from categories.models import Language, TopicTag
from categories.api.serializers import LanguageSerializer, TopicTagSerializer, MethodTagSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'image']

class CuratorSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_profile']
 

class TranslationSnippetSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()

    targetlanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = Translation
        fields = ['id', 'curator', 'curationdate', 'updated', 'targetlanguage', 'user_vote', 'upvote_count', 'downvote_count']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()


class TranslationSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)

    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    forks_count = serializers.SerializerMethodField()

    targetlanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = Translation
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_forks_count(self, instance):
        return instance.forks.count()


class TranscriptSnippetSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    translations = TranslationSnippetSerializer(many=True, read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    forks_count = serializers.SerializerMethodField()
    user_translation = serializers.SerializerMethodField()

    class Meta:
        model = Transcript
        fields = ['id', 'curator', 'curationdate', 'updated', 'translations', 'user_vote', 'upvote_count', 'downvote_count', 'forks_count', 'user_translation']
    
    def get_user_translation(self, instance):
        request = self.context.get("request")
        usertranslation = instance.translations.filter(curator=request.user.pk)
        if usertranslation.exists():
            return usertranslation[0].pk
        else:
            return 0

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_forks_count(self, instance):
        return instance.forks.count()


class TranscriptSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    translations = serializers.SerializerMethodField()
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    forks_count = serializers.SerializerMethodField()
    user_translation = serializers.SerializerMethodField()

    class Meta:
        model = Transcript
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']
    
    # This will only return those items that are published
    def get_translations(self, instance):
        request = self.context.get("request")
        translations = instance.translations.filter(published=True)
        return TranslationSnippetSerializer(translations, context = {"request": request}, many=True).data

    def get_user_translation(self, instance):
        request = self.context.get("request")
        usertranslation = instance.translations.filter(curator=request.user.pk)
        if usertranslation.exists():
            return usertranslation[0].pk
        else:
            return 0

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_forks_count(self, instance):
        return instance.forks.count()




class YouTubeElementSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    transcripts = serializers.SerializerMethodField()
    # transcripts = TranscriptSnippetSerializer(many=True, read_only=True)
    language = serializers.SlugRelatedField(
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
    user_transcript = serializers.SerializerMethodField()
    filtered = serializers.SerializerMethodField()
    
    notes = serializers.CharField(required=False, max_length=300, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=50), allow_empty=True, required=False)

    class Meta:
        model = YouTubeElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag']

    # This currently is only allowing published transcripts
    def get_transcripts(self, instance):
        request = self.context.get("request")
        transcripts = instance.transcripts.filter(published=True)
        return TranscriptSnippetSerializer(transcripts, context = {"request": request}, many=True).data

    def get_user_transcript(self, instance):
        request = self.context.get("request")
        usertranscript = instance.transcripts.filter(curator=request.user.pk)
        if usertranscript.exists():
            return usertranscript[0].pk
        else:
            return 0

    def get_filtered(self, instance):
        request = self.context.get("request")
        if instance.hidden.filter(pk=request.user.pk).exists():
            return True
        if instance.language not in request.user.user_profile.learninglanguage.all():
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
   
   #  def get_element_slug(self, instance):
   #      return instance.title


class AudioElementSerializer(serializers.ModelSerializer):
    transcripts = serializers.SerializerMethodField()
    curator = CuratorSerializer(read_only=True)
    language = serializers.SlugRelatedField(
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
    filtered = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    user_has_flagged = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField(max_length=50), allow_empty=True)
    user_transcript = serializers.SerializerMethodField()
    notes = serializers.CharField(required=False, max_length=300, allow_blank=True)
    # tags = serializers.ListField(child=serializers.CharField(max_length=50))

    class Meta:
        model = AudioElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag', 'suspended']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_filtered(self, instance):
        request = self.context.get("request")
        if instance.hidden.filter(pk=request.user.pk).exists():
            return True
        if instance.language not in request.user.user_profile.learninglanguage.all():
            print("In language")
            return True
        elif instance.topic not in request.user.user_profile.learningtopics.all():
            print("in topics")
            return True
        else:
            return False

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_transcripts(self, instance):
        request = self.context.get("request")
        transcripts = instance.transcripts.filter(published=True)
        return TranscriptSnippetSerializer(transcripts, context = {"request": request}, many=True).data

    def get_user_transcript(self, instance):
        request = self.context.get("request")
        usertranscript = instance.transcripts.filter(curator=request.user.pk)
        if usertranscript.exists():
            return usertranscript[0].pk
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



class MarkupSnippetSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()

    targetlanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = TextMarkup
        fields = ['id', 'curator', 'curationdate', 'updated', 'targetlanguage', 'user_vote', 'upvote_count', 'downvote_count']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

class TextMarkupSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    targetlanguage = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = TextMarkup
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']
    
    # This will only return those items that are published
    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()



class TextElementSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    translations = serializers.SerializerMethodField()
    markups = serializers.SerializerMethodField()
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    user_translation = serializers.SerializerMethodField()
    user_has_flagged = serializers.SerializerMethodField()
    user_has_saved = serializers.SerializerMethodField()
    user_has_hidden = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    user_markup = serializers.SerializerMethodField()

    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    topic = serializers.SlugRelatedField(
        queryset = TopicTag.objects.all(),
        read_only=False,
        slug_field='name'
    )


    class Meta:
        model = TextElement
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']
    
    # This will only return those items that are published
    def get_translations(self, instance):
        request = self.context.get("request")
        translations = instance.translations.filter(published=True)
        return TranslationSnippetSerializer(translations, context = {"request": request}, many=True).data

    def get_user_translation(self, instance):
        request = self.context.get("request")
        usertranslation = instance.translations.filter(curator=request.user.pk)
        if usertranslation.exists():
            return usertranslation[0].pk
        else:
            return 0

    def get_markups(self, instance):
        request = self.context.get("request")
        markups = instance.markups.filter(published=True)
        return MarkupSnippetSerializer(markups, context = {"request": request}, many=True).data

    def get_user_markup(self, instance):
        request = self.context.get("request")
        usertranscript = instance.markups.filter(curator=request.user.pk)
        if usertranscript.exists():
            return usertranscript[0].pk
        else:
            return 0

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvote.filter(pk=request.user.pk).exists():
            return 1
        elif instance.downvote.filter(pk=request.user.pk).exists():
            return -1
        else:
            return 0

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        return instance.flag.all().filter(flagger=request.user).exists()

    def get_flag_count(self, instance):
        return instance.flag.count()

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
