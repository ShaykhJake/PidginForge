from rest_framework import serializers
from users.models import CustomUser, Profile
from elements.models import YouTubeElement, AudioElement
from categories.models import Language, TopicTag
from categories.api.serializers import LanguageSerializer, TopicTagSerializer, MethodTagSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']

class CuratorSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['pk', 'username', 'user_profile']

class PostYouTubeSerializer(serializers.ModelSerializer):

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
    notes = serializers.CharField(required=False, max_length=300, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=50))

   
    class Meta:
        model = YouTubeElement
        fields = ['duration', 'title', 'videoid', 'thumbURL', 'language', 'topic', 'purpose', 'notes', 'tags']

    def create(self, user):
       user = CustomUser.objects.get(pk=user.pk)
       newYT = YouTubeElement(**self.validated_data)
       newYT.curator = user
       newYT.save()
       return True


class YouTubeElementSerializer(serializers.ModelSerializer):
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
    user_vote = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    
    notes = serializers.CharField(required=False, max_length=300, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=50))

    class Meta:
        model = YouTubeElement
        exclude = ['hidden', 'saved', 'upvote', 'downvote']

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





   # curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="youtube_curator")
   #  curationdate = models.DateTimeField(auto_now_add=True, editable=False)
   #  transcripts = models.ManyToManyField(Transcript, editable=False)

   #  purpose = models.CharField(max_length=305, default="", null=False)
   #  notes = models.CharField(max_length=305, default="", null=False)

   #  #Source Info
   #  videoid = models.CharField(max_length=100)
   #  thumbURL = models.CharField(max_length=200)
   #  # Length will be stored in seconds, then converted into HH:MM:SEC for display
   #  duration = models.PositiveIntegerField(default=0, editable=False) 

   #  # Title Defaults to What's Pulled in From Voice, but Can be Changed
   #  title = models.CharField(max_length=150, default="", null=False)
   #  slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

   #  # TODO - Consider whether or not to add a start/stop time?

   #  # Categories
   #  topic = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True)
   #  language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
   #  tags = ArrayField(models.CharField(max_length=100, blank=True), null=True)
   #  # TODO minorlanguage = models.ManyToManyField(Language)
    
   #  # Views is simply a one-up calculation every time a YTElement is loaded for viewing (TODO)
   #  views = models.PositiveIntegerField(default=0, editable=False)
    
   # #  Interactions
   #  saved = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="youtube_saved")
   #  hidden = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="youtube_hidden")