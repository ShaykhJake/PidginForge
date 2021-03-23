import json
from rest_framework import serializers
from users.models import CustomUser, Profile
from elements.models import (
    Element,
    Text,
    Audio,
    YouTube,
    ElementComment,
    CommentReply,

    YouTubeElement,
    AudioElement,
    Translation,
    Transcript,
    TextElement,
    TextMarkup,
    SavedVideo,
    SavedAudio,
    SavedText
)
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


class QuickTextElementSerializer(serializers.Serializer):
    rich_text = serializers.JSONField()
    plain_text = serializers.CharField()
    thumb = serializers.ImageField(read_only=True)


class QuickAudioElementSerializer(serializers.Serializer):
    audiofile = serializers.FileField(read_only=True)
    originalfilename = serializers.CharField(read_only=True)
    duration = serializers.IntegerField(read_only=True)
    thumb = serializers.ImageField(read_only=True)


class QuickYouTubeElementSerializer(serializers.Serializer):
    duration = serializers.IntegerField(read_only=True)
    video_id = serializers.CharField(read_only=True)
    thumb = serializers.URLField(read_only=True)


class QuickElementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    curator = CuratorSerializer(read_only=True)
    language = serializers.SerializerMethodField(read_only=True)
    curation_date = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(read_only=True)
    citation = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    sub_type = serializers.CharField(read_only=True)
    element = serializers.SerializerMethodField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)
    saved_count = serializers.SerializerMethodField(read_only=True)
    user_has_saved = serializers.BooleanField(read_only=True)
    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    user_vote = serializers.SerializerMethodField(read_only=True)
    transcript_count = serializers.SerializerMethodField(read_only=True)
    # flag_count = serializers.SerializerMethodField(read_only=True)

    def get_element(self, instance):
        if instance.sub_type == "Text":
            return QuickTextElementSerializer(instance.text).data
        elif instance.sub_type == "YouTube":
            return QuickYouTubeElementSerializer(instance.youtube).data
        elif instance.sub_type == "Audio":
            return QuickAudioElementSerializer(instance.audio).data
        else:
            return False

    def get_language(self, instance):
        return instance.language.name

    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_upvote_count(self, instance):
        return instance.upvotes.count()

    def get_downvote_count(self, instance):
        return instance.downvotes.count()

    def get_saved_count(self, instance):
        return instance.saves.count()

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.upvotes.filter(user=request.user).exists():
            return 1
        elif instance.downvotes.filter(user=request.user).exists():
            return -1
        else:
            return 0
    
    def get_transcript_count(self, instance):
        return instance.transcripts.count()

class ElementListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    curator = CuratorSerializer(read_only=True)
    language = serializers.SerializerMethodField(read_only=True)
    curation_date = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(read_only=True)
    citation = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    sub_type = serializers.CharField(read_only=True)
    element = serializers.SerializerMethodField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)
    saved_count = serializers.SerializerMethodField(read_only=True)
    user_has_saved = serializers.BooleanField(read_only=True)
    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    transcript_count = serializers.SerializerMethodField(read_only=True)
    # user_vote = serializers.SerializerMethodField(read_only=True)
    # flag_count = serializers.SerializerMethodField(read_only=True)

    def get_element(self, instance):
        if instance.sub_type == "Text":
            return QuickTextElementSerializer(instance.text).data
        elif instance.sub_type == "YouTube":
            return QuickYouTubeElementSerializer(instance.youtube).data
        elif instance.sub_type == "Audio":
            return QuickAudioElementSerializer(instance.audio).data
        else:
            return False

    def get_language(self, instance):
        return instance.language.name

    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_upvote_count(self, instance):
        return instance.upvotes.count()

    def get_downvote_count(self, instance):
        return instance.downvotes.count()

    def get_saved_count(self, instance):
        return instance.saves.count()

    def get_comment_count(self, instance):
        return instance.comments.count()
    # def get_user_has_saved(self, instance):
    #     # request = self.context.get("request")
    #     return instance.user_saved

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if instance.user_upvote:
            return 1
        elif instance.user_downvote:
            return -1
        else:
            return 0

    def get_transcript_count(self, instance):
        return instance.transcripts.count()




class ElementAudioSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(
        queryset=Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = Audio
        fields = ['curator', 'title', 'description', 'citation', 'language','thumb',
                  'sub_type', 'audiofile', 'duration', 'originalfilename', 'slug']
        read_only_fields = ['slug', 'curator']

    def create(self, validated_data):
        """
        Create and return a new `Audio Element` instance, given the validated data.
        """
        request = self.context.get("request")
        tags = self.initial_data['tags']
        tag_array = []
        if tags:
            tag_array = tags.split(",")
        else:
            tag_array = None

        return Audio.objects.create(**validated_data, curator=request.user, tags=(tag_array))

    def update(self, instance, validated_data):
        """Here we need special treatment for tags due to the fact that this API post is
        coming in as FormData. Javascript JSON.Stringifies the tags field, and here 
        we need to parse it out.
        """
        tags = self.initial_data['tags']
        tag_array = []
        if tags:
            tag_array = tags.split(",")
            instance.tags = tag_array
        else:
            instance.tags = None
        instance.save()
        return instance


class ElementTextSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(
        queryset=Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = Text
        fields = ['curator', 'title', 'description', 'citation','thumb',
                  'rich_text', 'plain_text', 'language', 'sub_type', 'tags', 'slug']
        read_only_fields = ['slug', 'curator']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print("hello!")
        request = self.context.get("request")
        return Text.objects.create(**validated_data, curator=request.user)


class ElementYouTubeSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(
        queryset=Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = YouTube
        fields = ['curator', 'title', 'description', 'citation', 'thumb',
                  'video_id', 'duration', 'language', 'sub_type', 'tags', 'slug']
        read_only_fields = ['slug', 'curator']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        request = self.context.get("request")
        return YouTube.objects.create(**validated_data, curator=request.user)

class ElementCommentSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curation_date = serializers.SerializerMethodField(read_only=True)
    element = serializers.SlugRelatedField(
        queryset=Element.objects.all(),
        read_only=False,
        slug_field='pk'
    )

    class Meta:
        model = ElementComment
        # fields = '__all__'
        exclude = ['suspended']
        read_only_fields = ['curator', 'updated', 'curation_date']
    
    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")


class CommentReplySerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curation_date = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SlugRelatedField(
        queryset=ElementComment.objects.all(),
        read_only=False,
        slug_field='pk'
    )

    class Meta:
        model = CommentReply
        # fields = '__all__'
        exclude = ['suspended']
        read_only_fields = ['curator', 'updated', 'curation_date']
    
    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")



class TranscriptSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curation_date = serializers.SerializerMethodField(read_only=True)
    updated = serializers.SerializerMethodField(read_only=True)
    forks_count = serializers.SerializerMethodField(read_only=True)
    # translations = serializers.SerializerMethodField(read_only=True)
    # user_vote = serializers.SerializerMethodField(read_only=True)
    # upvote_count = serializers.SerializerMethodField(read_only=True)
    # downvote_count = serializers.SerializerMethodField(read_only=True)
    # user_translation = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transcript
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    # This will only return those items that are published
    def get_translations(self, instance):
        request = self.context.get("request")
        translations = instance.translations.filter(
            published=True).select_related('curator')
        return TranslationSnippetSerializer(translations, context={"request": request}, many=True).data
        # return TranslationSnippetSerializer(instance.translations.all(), context={"request": request}, many=True).data

    def get_user_translation(self, instance):
        request = self.context.get("request")
        for translation in instance.translations.all():
            if translation.curator == request.user:
                return translation.pk
        return 0

    def get_curation_date(self, instance):
        return instance.curation_date.strftime("%B %d, %Y")

    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user in instance.upvote.all():
            return 1
        elif request.user in instance.downvote.all():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_forks_count(self, instance):
        return instance.forks.count()

"""OLD STUFF"""


class TranslationSnippetSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    targetlanguage = serializers.SerializerMethodField()

    class Meta:
        model = Translation
        fields = ['id', 'curator', 'curationdate', 'updated',
                  'targetlanguage', 'user_vote', 'upvote_count', 'downvote_count']
        read_only_fields = fields

    def get_targetlanguage(self, instance):
        return instance.targetlanguage.name

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
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
        queryset=Language.objects.all(),
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
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
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
        fields = ['id', 'curator', 'curationdate', 'updated', 'translations', 'user_vote',
                  'upvote_count', 'downvote_count', 'forks_count', 'user_translation']
        read_only_fields = fields

    def get_user_translation(self, instance):
        request = self.context.get("request")
        for translation in instance.translations.all():
            if translation.curator == request.user:
                return translation.pk
        return 0

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user in instance.upvote.all():
            return 1
        elif request.user in instance.downvote.all():
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
        queryset=Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    topic = serializers.SlugRelatedField(
        queryset=TopicTag.objects.all(),
        read_only=False,
        slug_field='name'
    )

    curationdate = serializers.SerializerMethodField(read_only=True)
    saved_count = serializers.SerializerMethodField(read_only=True)
    user_has_saved = serializers.SerializerMethodField(read_only=True)
    user_has_hidden = serializers.SerializerMethodField(read_only=True)
    user_vote = serializers.SerializerMethodField(read_only=True)
    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    flag_count = serializers.SerializerMethodField(read_only=True)
    user_has_flagged = serializers.SerializerMethodField(read_only=True)
    user_transcript = serializers.SerializerMethodField(read_only=True)
    notes = serializers.CharField(
        required=False, max_length=300, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)

    class Meta:
        model = YouTubeElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag']

    # This currently is only allowing published transcripts
    def get_transcripts(self, instance):
        request = self.context.get("request")
        # transcripts = Transcript.objects.filter(youtube_transcripts=instance)
        transcripts = instance.transcripts.filter(
            published=True).select_related('curator')
        return TranscriptSnippetSerializer(transcripts, context={"request": request}, many=True).data

    def get_user_transcript(self, instance):
        request = self.context.get("request")
        for transcript in instance.transcripts.all():
            if transcript.curator == request.user:
                return transcript.pk
        return 0

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
            return -1
        else:
            return 0

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        for flag in instance.flag.all():
            if flag.flagger == request.user:
                return True
        return False

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedvideo_set.count()

    def get_user_has_saved(self, instance):
        return instance.savedvideo_set.exists()

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return request.user in instance.hidden.all()


class YouTubeListSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    transcripts = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
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

    notes = serializers.CharField(
        required=False, max_length=300, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)

    class Meta:
        model = YouTubeElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag']

    # This currently is only allowing published transcripts
    def get_transcripts(self, instance):
        return instance.transcripts.count()

    def get_user_transcript(self, instance):
        request = self.context.get("request")
        for transcript in instance.transcripts.all():
            if transcript.curator == request.user:
                return transcript.id
        return 0
        # usertranscript = Transcript.objects.filter(curator=request.user).filter(youtube_transcripts=instance).first()
        # if usertranscript:
        #     return usertranscript.pk
        # else:
        #     return 0

    def get_language(self, instance):
        return instance.language.name

    def get_topic(self, instance):
        return instance.topic.name

    def get_filtered(self, instance):
        request = self.context.get("request")
        learninglanguages = self.context.get("learninglanguages")
        # if instance.hidden.filter(pk=request.user.pk).exists():
        #     return True
        if instance.language not in learninglanguages:
            return True
        else:
            return False

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
            return -1
        else:
            return 0

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        return request.user.pk in instance.flag.all()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedvideo_set.count()

    def get_user_has_saved(self, instance):
        return instance.savedvideo_set.exists()

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return request.user.pk in instance.hidden.all()


class AudioElementSerializer(serializers.ModelSerializer):
    transcripts = serializers.SerializerMethodField()
    curator = CuratorSerializer(read_only=True)
    language = serializers.SlugRelatedField(
        queryset=Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    topic = serializers.SlugRelatedField(
        queryset=TopicTag.objects.all(),
        read_only=False,
        slug_field='name'
    )

    curationdate = serializers.SerializerMethodField(read_only=True)
    saved_count = serializers.SerializerMethodField(read_only=True)
    user_has_saved = serializers.SerializerMethodField(read_only=True)
    user_has_hidden = serializers.SerializerMethodField(read_only=True)
    user_vote = serializers.SerializerMethodField(read_only=True)
    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    flag_count = serializers.SerializerMethodField(read_only=True)
    user_has_flagged = serializers.SerializerMethodField(read_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50), allow_empty=True)
    user_transcript = serializers.SerializerMethodField(read_only=True)
    notes = serializers.CharField(
        required=False, max_length=300, allow_blank=True)

    class Meta:
        model = AudioElement
        exclude = ['hidden', 'saved', 'upvote',
                   'downvote', 'flag', 'suspended']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user in instance.upvote.all():
            return 1
        elif request.user in instance.downvote.all():
            return -1
        else:
            return 0

    def get_transcripts(self, instance):
        request = self.context.get("request")
        transcripts = instance.transcripts.filter(published=True)
        return TranscriptSnippetSerializer(transcripts, context={"request": request}, many=True).data

    def get_user_transcript(self, instance):
        request = self.context.get("request")
        for transcript in instance.transcripts.all():
            if transcript.curator == request.user:
                return transcript.pk
        return 0

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        for flag in instance.flag.all():
            if flag.flagger == request.user:
                return True
        return False

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedaudio_set.count()

    def get_user_has_saved(self, instance):
        return instance.savedaudio_set.exists()

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return request.user in instance.hidden.all()
        # return instance.hidden.filter(pk=request.user.pk).exists()


class AudioListSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    transcripts = serializers.SerializerMethodField(read_only=True)
    language = serializers.SerializerMethodField(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    saved_count = serializers.SerializerMethodField(read_only=True)
    user_has_saved = serializers.SerializerMethodField(read_only=True)
    user_has_hidden = serializers.SerializerMethodField(read_only=True)
    user_vote = serializers.SerializerMethodField(read_only=True)
    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    flag_count = serializers.SerializerMethodField(read_only=True)
    user_has_flagged = serializers.SerializerMethodField(read_only=True)
    filtered = serializers.SerializerMethodField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)

    class Meta:
        model = AudioElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag']

    # This currently is only allowing published transcripts
    def get_transcripts(self, instance):
        return instance.transcripts.count()

    def get_language(self, instance):
        return instance.language.name

    def get_filtered(self, instance):
        request = self.context.get("request")
        learninglanguages = self.context.get("learninglanguages")
        if instance.language not in learninglanguages:
            return True
        else:
            return False

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
            return -1
        else:
            return 0

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        return request.user.pk in instance.flag.all()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedaudio_set.count()

    def get_user_has_saved(self, instance):
        return instance.savedaudio_set.exists()

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return request.user.pk in instance.hidden.all()


class TextListSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    translations = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
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
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)

    class Meta:
        model = TextElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag']

    # This currently is only allowing published transcripts
    def get_translations(self, instance):
        return instance.translations.count()

    def get_language(self, instance):
        return instance.language.name

    def get_filtered(self, instance):
        request = self.context.get("request")
        learninglanguages = self.context.get("learninglanguages")
        if instance.language not in learninglanguages:
            return True
        else:
            return False

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
            return -1
        else:
            return 0

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        return request.user.pk in instance.flag.all()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedtext_set.count()

    def get_user_has_saved(self, instance):

        return instance.savedtext_set.exists()

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return request.user.pk in instance.hidden.all()


class MarkupSnippetSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()

    targetlanguage = serializers.SlugRelatedField(
        queryset=Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = TextMarkup
        fields = ['id', 'curator', 'curationdate', 'updated',
                  'targetlanguage', 'user_vote', 'upvote_count', 'downvote_count']
        read_only_fields = fields

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
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
        queryset=Language.objects.all(),
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
        request = self.context.get("request")
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
            return -1
        else:
            return 0

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()


class TextElementSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    translations = serializers.SerializerMethodField(read_only=True)
    markups = serializers.SerializerMethodField(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    user_translation = serializers.SerializerMethodField()
    user_has_flagged = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()
    user_has_saved = serializers.SerializerMethodField()
    user_has_hidden = serializers.SerializerMethodField()
    flag_count = serializers.SerializerMethodField()
    user_markup = serializers.SerializerMethodField()

    language = serializers.SlugRelatedField(
        queryset=Language.objects.all(),
        read_only=False,
        slug_field='name'
    )

    topic = serializers.SlugRelatedField(
        queryset=TopicTag.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = TextElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote',
                   'flag', 'suspended', 'charactercount']

    # This will only return those items that are published
    def get_translations(self, instance):
        request = self.context.get("request")
        translations = instance.translations.filter(published=True)
        return TranslationSnippetSerializer(translations, context={"request": request}, many=True).data

    def get_user_translation(self, instance):
        request = self.context.get("request")
        for translation in instance.translations.all():
            if translation.curator == request.user:
                return translation.pk
        return 0

    def get_markups(self, instance):
        request = self.context.get("request")
        markups = instance.markups.filter(published=True).select_related(
            'curator', 'targetlanguage', 'forkparent').prefetch_related('upvote', 'downvote')
        return MarkupSnippetSerializer(markups, context={"request": request}, many=True).data

    def get_user_markup(self, instance):
        request = self.context.get("request")
        for markup in instance.markups.all():
            if markup.curator == request.user:
                return markup.pk
        return 0

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_user_vote(self, instance):
        request = self.context.get("request")
        if request.user.pk in instance.upvote.all():
            return 1
        elif request.user.pk in instance.downvote.all():
            return -1
        else:
            return 0

    def get_user_has_flagged(self, instance):
        request = self.context.get("request")
        for flag in instance.flag.all():
            if flag.flagger == request.user:
                return True
        return False

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedtext_set.count()

    def get_user_has_saved(self, instance):
        request = self.context.get("request")
        for saved in instance.savedtext_set.all():
            if saved.curator == request.user:
                return True
        return False

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return request.user in instance.hidden.all()


class QuickVideoSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    language = serializers.SerializerMethodField(read_only=True)
    topic = serializers.SerializerMethodField(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    saved_count = serializers.SerializerMethodField(read_only=True)
    # user_has_saved = serializers.SerializerMethodField(read_only=True)
    # user_has_hidden = serializers.SerializerMethodField(read_only=True)
    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    flag_count = serializers.SerializerMethodField(read_only=True)
    transcripts = serializers.SerializerMethodField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)

    class Meta:
        model = YouTubeElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag', 'notes']

    # This currently is only allowing published transcripts
    def get_language(self, instance):
        return instance.language.name

    def get_topic(self, instance):
        return instance.topic.name

    def get_transcripts(self, instance):
        return instance.transcripts.count()

    def get_filtered(self, instance):
        request = self.context.get("request")
        if instance.hidden.filter(pk=request.user.pk).exists():
            return True
        if instance.language not in request.user.user_profile.learninglanguage.all():
            return True
        else:
            return False

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedvideo_set.count()

    def get_user_has_saved(self, instance):
        return instance.savedvideo_set.exists()

    def get_user_has_hidden(self, instance):
        request = self.context.get("request")
        return instance.hidden.filter(pk=request.user.pk).exists()


class QuickAudioSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    language = serializers.SerializerMethodField(read_only=True)
    topic = serializers.SerializerMethodField(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    saved_count = serializers.SerializerMethodField(read_only=True)
    # user_has_saved = serializers.SerializerMethodField(read_only=True)
    # user_has_hidden = serializers.SerializerMethodField(read_only=True)
    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    flag_count = serializers.SerializerMethodField(read_only=True)
    transcripts = serializers.SerializerMethodField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)

    class Meta:
        model = AudioElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag', 'notes']

    # This currently is only allowing published transcripts
    def get_language(self, instance):
        return instance.language.name

    def get_topic(self, instance):
        return instance.topic.name

    def get_transcripts(self, instance):
        return instance.transcripts.count()

    def get_filtered(self, instance):
        request = self.context.get("request")
        if instance.hidden.filter(pk=request.user.pk).exists():
            return True
        if instance.language not in request.user.user_profile.learninglanguage.all():
            return True
        else:
            return False

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedaudio_set.count()


class QuickTextSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    language = serializers.SerializerMethodField(read_only=True)
    topic = serializers.SerializerMethodField(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    saved_count = serializers.SerializerMethodField(read_only=True)
    # user_has_saved = serializers.SerializerMethodField(read_only=True)
    # user_has_hidden = serializers.SerializerMethodField(read_only=True)
    upvote_count = serializers.SerializerMethodField(read_only=True)
    downvote_count = serializers.SerializerMethodField(read_only=True)
    flag_count = serializers.SerializerMethodField(read_only=True)
    translations = serializers.SerializerMethodField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField(
        max_length=50), allow_empty=True, required=False)

    class Meta:
        model = TextElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote', 'flag', 'notes']

    # This currently is only allowing published transcripts
    def get_language(self, instance):
        return instance.language.name

    def get_topic(self, instance):
        return instance.topic.name

    def get_translations(self, instance):
        return instance.translations.count()

    def get_filtered(self, instance):
        request = self.context.get("request")
        if instance.hidden.filter(pk=request.user.pk).exists():
            return True
        if instance.language not in request.user.user_profile.learninglanguage.all():
            return True
        else:
            return False

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")

    def get_flag_count(self, instance):
        return instance.flag.count()

    def get_upvote_count(self, instance):
        return instance.upvote.count()

    def get_downvote_count(self, instance):
        return instance.downvote.count()

    def get_saved_count(self, instance):
        return instance.savedtext_set.count()
