from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, action
from django.db.models import Prefetch, Q, Exists, OuterRef, Count
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required

from elements.api.serializers import (
    QuickElementSerializer,
    ElementListSerializer,
    ElementTextSerializer,
    ElementAudioSerializer,
    ElementYouTubeSerializer,
    ElementCommentSerializer,
    CommentReplySerializer,

    YouTubeElementSerializer,
    YouTubeListSerializer,
    AudioElementSerializer,
    AudioListSerializer,
    TextElementSerializer,
    TextListSerializer,
    TranscriptSerializer,
    TranscriptSnippetSerializer,
    TranslationSerializer,
    TranslationSnippetSerializer,
    TextMarkupSerializer,
    MarkupSnippetSerializer,

)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from elements.models import (
    Element,
    ElementComment,
    CommentReply,
    Text,
    Audio,
    YouTube,
    ElementUpVote,
    ElementDownVote,
    ElementSave,
    ElementHide,

    YouTubeElement,
    Transcript,
    Translation,
    AudioElement,
    TextElement,
    TextMarkup,
    SavedVideo,
    SavedText,
    SavedAudio
)

import django_filters as django_filter


class IsCuratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.curator == request.user


class IsPublishedOrAuthorOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.curator == request.user:
            return True
        if obj.published == False and obj.curator is not request.user:
            return False

class ElementFilter(django_filter.FilterSet):
    tags = django_filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Element
        fields = ('sub_type', 'language', 'curator__username', 'tags')
    

class ElementList(generics.ListAPIView):
    model = Element
    serializer_class = ElementListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ElementFilter
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['title', 'sub_type',
                       'curation_date', 'updated', 'language']
    ordering = ['-curation_date']

    def get_queryset(self):
        user = self.request.user
        user_upvote_queryset = ElementUpVote.objects.filter(user=user)
        user_downvote_queryset = ElementDownVote.objects.filter(user=user)
        queryset = Element.objects.filter(suspended=False).exclude(hides__user=user).select_related(
            'curator__user_profile', 'language'
        ).prefetch_related(
            'saves', 'upvotes', 'downvotes', 'comments', 'transcripts'
        ).annotate(
            user_has_saved=Exists(
                ElementSave.objects.filter(
                    element=OuterRef('pk'),
                    user=user
                ))
        ).prefetch_related(
            Prefetch('upvotes', queryset=user_upvote_queryset, to_attr='user_upvote')
        ).prefetch_related(
            Prefetch('downvotes', queryset=user_downvote_queryset, to_attr='user_downvote')
        ).select_subclasses()
        by_preference = self.request.query_params.get('by_preference', None)
        by_saves = self.request.query_params.get('saved', None)
        if by_preference is not None:
            queryset = queryset.filter(language__in=user.user_profile.learninglanguage.all())
        if by_saves is not None:
            queryset = queryset.filter(saves__user=user).order_by('-saves__created')
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}



class ElementCommentFilter(django_filter.FilterSet):
    tags = django_filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ElementComment
        fields = ('element','curator')
    

class ElementCommentList(generics.ListAPIView):
    model = ElementComment
    serializer_class = ElementCommentSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ElementCommentFilter
    search_fields = ['plain_text']
    ordering_fields = ['curation_date', 'updated']
    ordering = ['-curation_date']

    def get_queryset(self):
        user = self.request.user
        queryset = ElementComment.objects.filter(suspended=False).select_related(
            'curator__user_profile'
        ).prefetch_related(
            'replies'
        )

    def get_serializer_context(self):
        return {'request': self.request}

class CommentReplyFilter(django_filter.FilterSet):
    tags = django_filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CommentReply
        fields = ('comment','curator')
    

class CommentReplyList(generics.ListAPIView):
    model = CommentReply
    serializer_class = CommentReplySerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentReplyFilter
    search_fields = ['plain_text']
    ordering_fields = ['curation_date', 'updated']
    ordering = ['-curation_date']

    def get_queryset(self):
        user = self.request.user
        queryset = CommentReply.objects.filter(suspended=False).select_related(
            'curator__user_profile', 'comment'
        )

    def get_serializer_context(self):
        return {'request': self.request}

class TranscriptFilter(django_filter.FilterSet):
    tags = django_filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Transcript
        fields = ('element','curator')
    

class TranscriptList(generics.ListAPIView):
    model = Transcript
    serializer_class = TranscriptSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TranscriptFilter
    search_fields = ['plain_text']
    ordering_fields = ['curation_date', 'updated']
    ordering = ['-curation_date']

    def get_queryset(self):
        user = self.request.user
        queryset = Transcript.objects.filter(Q(published=True) | Q(curator=self.request.user)).select_related(
            'curator__user_profile'
        )

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET'])
def get_element(request, slug):
    user_upvote_queryset = ElementUpVote.objects.filter(user=request.user)
    user_downvote_queryset = ElementDownVote.objects.filter(user=request.user)
    element = get_object_or_404(
        Element.objects.select_related(
            'curator__user_profile'
        ).prefetch_related(
            'saves', 'upvotes','downvotes'
        ).annotate(
            user_has_saved=Exists(
                ElementSave.objects.filter(
                    element=OuterRef('pk'), 
                    user=request.user
                ))
        ).prefetch_related(
            Prefetch('upvotes', queryset=user_upvote_queryset, to_attr='user_upvote')
        ).prefetch_related(
            Prefetch('downvotes', queryset=user_downvote_queryset, to_attr='user_downvote')
        ), slug=slug
        )
    context = {
        "request": request
    }
    return Response(QuickElementSerializer(element, context=context).data)

class ElementViewSet(viewsets.ModelViewSet):
    """This viewset covers text, audio, and youtube in one"""
    queryset = Element.objects.all().order_by("-curation_date")
    lookup_field = "slug"
    serializer_class = QuickElementSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def create(self, request, *args, **kwargs):
        if request.data['sub_type'] == 'Text':
            serializer = ElementTextSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                element = serializer.save()
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.data['sub_type'] == 'Audio':
            parser_classes = (MultiPartParser, FormParser, )
            serializer = ElementAudioSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                element = serializer.save()
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.data['sub_type'] == 'YouTube':
            serializer = ElementYouTubeSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                element = serializer.save()
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(QuickElementSerializer(element, context={"request":request}).data)

    def partial_update(self, request, slug):
        if request.data['sub_type'] == 'Text':
            element = get_object_or_404(Text, slug=slug)
            serializer = ElementTextSerializer(element, data=request.data, partial=True)
            if serializer.is_valid():
                element = serializer.save()
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.data['sub_type'] == 'Audio':
            parser_classes = (MultiPartParser, FormParser, )
            element = get_object_or_404(Audio, slug=slug)
            serializer = ElementAudioSerializer(
                element, data=request.data, partial=True)
            if serializer.is_valid():
                element = serializer.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.data['sub_type'] == 'YouTube':
            element = get_object_or_404(YouTube, slug=slug)
            serializer = ElementYouTubeSerializer(element, data=request.data, partial=True)
            if serializer.is_valid():
                element = serializer.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(QuickElementSerializer(element, context={"request":request}).data)

@api_view(['POST'])
def element_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                Element, slug=request.data['slug'])

            if request.data['vote'] == "up":
                try:
                    downvote = ElementDownVote.objects.get(user=request.user, element=element)
                except ElementDownVote.DoesNotExist:
                    pass
                else:
                    downvote.delete()
                try:
                    upvote = ElementUpVote.objects.get(user=request.user, element=element)
                except ElementUpVote.DoesNotExist:
                    ElementUpVote.objects.create(user=request.user, element=element)
                resdata['newuservote'] = 1
                resdata['message'] = "Successfully upvoted the youtube element!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                try:
                    upvote = ElementUpVote.objects.get(user=request.user, element=element)
                except ElementUpVote.DoesNotExist:
                    pass
                else:
                    upvote.delete()
                try:
                    downvote = ElementDownVote.objects.get(user=request.user, element=element)
                except ElementDownVote.DoesNotExist:
                    downvote = ElementDownVote.objects.create(user=request.user, element=element)
                resdata['newuservote'] = -1
                resdata['message'] = "Successfully downvoted the youtube element!"
                resdata['success'] = True
            resdata['newupcount'] = element.upvotes.count()
            resdata['newdowncount'] = element.downvotes.count()

        return Response(resdata)

@api_view(['POST'])
def element_togglesave(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            try: 
                element = get_object_or_404(Element, pk=request.data['pk'])
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                saved = ElementSave.objects.filter(user=request.user,element=element)
                if saved:
                    saved.delete()
                    resdata['message'] = "Successfully removed item from saved list"
                    resdata['success'] = True
                else:
                    ElementSave.objects.create(user=request.user, element=element)
                    resdata['message'] = "Successfully added item to saved list"
                    resdata['success'] = True
    return Response(resdata)

@api_view(['POST'])
def element_togglehide(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            try: 
                element = get_object_or_404(Element, pk=request.data['pk'])
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                hidden = ElementHide.objects.filter(user=request.user,element=element)
                if hidden:
                    hidden.delete()
                    resdata['message'] = "Successfully removed item from hidden list"
                    resdata['success'] = True
                    resdata['hidden'] = False
                else:
                    ElementHide.objects.create(user=request.user, element=element)
                    resdata['message'] = "Successfully added item to hidden list"
                    resdata['success'] = True
                    resdata['hidden'] = True
    return Response(resdata)


@api_view(['GET'])
def saved_element_list(request):
    if request.method == 'GET':
        resdata = {}
        if request.user.is_authenticated:
            elements = Element.objects.prefetch_related(
                    Prefetch('saves', queryset=ElementSave.objects.filter(user=request.user))
                ).filter(suspended=False).exclude(hides__user=request.user).select_related(
                'curator__user_profile', 'language'
            ).prefetch_related(
                'saves', 'upvotes','downvotes'
            ).select_subclasses()

            serializer_context = {"request": request}
            serializer = ElementListSerializer(
                elements, many=True, context=serializer_context)
            return Response(serializer.data)



class ElementCommentViewSet(viewsets.ModelViewSet):
    queryset = ElementComment.objects.all().order_by("-curation_date")
    lookup_field = "pk"
    serializer_class = ElementCommentSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = ElementCommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            comment = serializer.save(curator=request.user)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(ElementCommentSerializer(comment, context={"request":request}).data)

    def partial_update(self, request, pk):
        comment = get_object_or_404(ElementComment, pk=pk)
        serializer = ElementCommentSerializer(comment, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(ElementCommentSerializer(comment, context={"request": request}).data)

class CommentReplyViewSet(viewsets.ModelViewSet):
    queryset = CommentReply.objects.select_related('curator','curator__user_profile','comment__curator').order_by("-curation_date")
    lookup_field = "pk"
    serializer_class = CommentReplySerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = CommentReplySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            reply = serializer.save(curator=request.user)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(CommentReplySerializer(reply, context={"request":request}).data)

    def partial_update(self, request, pk):
        reply = get_object_or_404(CommentReply, pk=pk)
        serializer = CommentReplySerializer(reply, data=request.data, context={"request": request}, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(CommentReplySerializer(reply, context={"request": request}).data)


"""OLD STUFF Below"""


###### YOUTUBE ELEMENT VIEWS #######


class YouTubeViewSet(viewsets.ModelViewSet):

    queryset = YouTubeElement.objects.all().filter(
        suspended=False,
    ).select_related(
        'curator', 'curator__user_profile', 'language', 'topic'
    ).prefetch_related(
        'upvote', 'downvote', 'hidden', 'flag', 'savedvideo_set', 'transcripts'
    ).order_by("-curationdate")

    lookup_field = "slug"
    serializer_class = YouTubeElementSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # This list is currently factoring in user preferences and filtering by learning languages/topics
    def list(self, request):
        learninglanguages = request.user.user_profile.learninglanguage.all()
        user_saved = SavedVideo.objects.filter(curator=request.user)
        queryset = YouTubeElement.objects.filter(
            suspended=False,
            #   language__in = userlanguages,
            #   topic__in = usertopics,
        ).select_related(
            'curator', 'curator__user_profile', 'language', 'topic'
        ).prefetch_related(
            'transcripts', 'hidden', 'upvote', 'downvote', 'flag',
        ).prefetch_related(
            Prefetch('savedvideo_set', queryset=user_saved)
        ).order_by("-curationdate")

        serializer_context = {
            "request": request, "learninglanguages": learninglanguages}

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = YouTubeListSerializer(
                page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = YouTubeListSerializer(
            queryset, many=True, context=serializer_context)
        return Response(serializer.data)


@api_view(['POST'])
def youtube_check(request):
    resdata = {}
    if request.method == 'POST':
        videoid = request.data['videoid']
        if videoid:
            items = YouTubeElement.objects.filter(videoid=videoid)
            if items.count() == 0:
                resdata['available'] = True
                resdata['message'] = "That youtube does not yet exist in the database!"
            else:
                resdata['available'] = False
                resdata['message'] = "Video already exists in database as..."
                resdata['slug'] = items[0].slug
                resdata['title'] = items[0].title
                # TODO Add in the link to the object that already exists
    return Response(resdata)

# THIS IS THE OLD FORM FOR ATTACHING A SAVE WITHIN THE MODEL


@api_view(['POST'])
def youtube_togglesaved(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                YouTubeElement, pk=int(request.data['pk']))
            if request.user in element.saved.all():
                element.saved.remove(request.user)
                element.save()
                resdata['message'] = "Successfully removed item from saved list"
                resdata['success'] = True
            else:
                element.saved.add(request.user)
                element.save()
                resdata['message'] = "Successfully added item to saved list"
                resdata['success'] = True
    return Response(resdata)


@api_view(['POST'])
def video_togglesaved(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                YouTubeElement, pk=int(request.data['pk']))
            savings = SavedVideo.objects.filter(youtube_element=int(
                request.data['pk']), curator=request.user).first()
            if savings:
               #  print("Element Deleted")
                savings.delete()
                resdata['message'] = "Successfully removed item from saved list"
                resdata['success'] = True
            else:
               #  print("Element Saved")
                savings = SavedVideo.objects.create(
                    youtube_element=element, curator=request.user)
                resdata['message'] = "Successfully added item to saved list"
                resdata['success'] = True
        return Response(resdata)


@api_view(['POST'])
def youtube_togglehidden(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                YouTubeElement, pk=int(request.data['pk']))
            if request.user in element.hidden.all():
                element.hidden.remove(request.user)
                element.save()
                resdata['message'] = "Successfully removed item from hidden list"
                resdata['success'] = True
            else:
                element.hidden.add(request.user)
                element.save()
                resdata['message'] = "Successfully added item to hidden list"
                resdata['success'] = True
    return Response(resdata)


@api_view(['POST'])
def youtube_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                YouTubeElement, slug=request.data['slug'])
            if request.data['vote'] == "up":
                resdata['newuservote'] = 1
                if request.user in element.downvote.all():
                    element.downvote.remove(request.user)
                    element.save()
                if request.user not in element.upvote.all():
                    element.upvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully upvoted the youtube element!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                resdata['newuservote'] = -1
                if request.user in element.upvote.all():
                    element.upvote.remove(request.user)
                    element.save()
                if request.user not in element.downvote.all():
                    element.downvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully downvoted the youtube element!"
                resdata['success'] = True
            resdata['newupcount'] = element.upvote.all().count()
            resdata['newdowncount'] = element.downvote.all().count()

        return Response(resdata)


# ARCHIVES
# NOW DEFUNCT...ONLY KEEPING FOR REFERENCE BECAUSE IT ONCE WORKED
@api_view(['GET', 'POST', 'PATCH'])
def youtube_view(request, slug):
    # Get
    if request.method == 'GET':
        youtube = YouTubeElement.objects.get(slug=slug)
        serializer = YouTubeElementSerializer(youtube)
        resdata = {}
        resdata['message'] = "Hi there"
        resdata['available'] = True
        return Response(resdata)

    # Post
    if request.method == 'POST':
        resdata = {}
        # print(request.data)
        if request.user.is_authenticated:
            # print(request.data)
            serializer = YouTubeElementSerializer(data=request.data)

            if serializer.is_valid():
                if serializer.create(request.user):
                    resdata['message'] = "Your youtube element has been added to the database!"
                    resdata['success'] = True
                else:
                    resdata['message'] = "There was a problem adding your video element!"
                    resdata['success'] = False
            else:
                resdata['message'] = "Your request was invalid!"
                resdata['success'] = False
        else:
            resdata['message'] = "You must be an authenticated user to post to the database!"
            resdata['success'] = False
        # print(resdata)
        return Response(resdata)


@api_view(['GET'])
def youtube_list(request):
    queryset = YouTubeElement.objects.all()
    serializer = YouTubeElementSerializer(queryset, many=True)
    return Response(serializer.data)


class YouTubeListAPIView(generics.ListAPIView):
    serializer_class = YouTubeElementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #   kwarg_slug = self.kwargs.get("slug")
        return YouTubeElement.objects.all().order_by("-curationdate")


####### AUDIO ELEMENT VIEWS ############
class AudioViewSet(viewsets.ModelViewSet):
    # queryset = AudioElement.objects.all().order_by("-curationdate")
    queryset = AudioElement.objects.filter(
        suspended=False,
        #   language__in = userlanguages,
        #   topic__in = usertopics,
    ).select_related(
        'curator', 'curator__user_profile', 'language',
    ).prefetch_related(
        'transcripts', 'hidden', 'upvote', 'downvote', 'flag', 'savedaudio_set'
    ).order_by("-curationdate")
    lookup_field = "slug"
    serializer_class = AudioElementSerializer
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, slug):
        element = get_object_or_404(AudioElement, slug=slug)
        serializer_context = {"request": request}
        serializer = AudioElementSerializer(
            element, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        updatedserializer = AudioElementSerializer(
            element, context=serializer_context)
        return Response(updatedserializer.data)

    # This list is currently factoring in user preferences and filtering by learning languages/topics

    def list(self, request):
        learninglanguages = request.user.user_profile.learninglanguage.all()
        user_saved = SavedAudio.objects.filter(curator=request.user)

        queryset = AudioElement.objects.filter(
            suspended=False,
            #   language__in = userlanguages,
            #   topic__in = usertopics,
        ).select_related(
            'curator', 'curator__user_profile', 'language',
        ).prefetch_related(
            'transcripts', 'hidden', 'upvote', 'downvote', 'flag'
        ).prefetch_related(
            Prefetch('savedaudio_set', queryset=user_saved)
        ).order_by("-curationdate")

        serializer_context = {
            "request": request, "learninglanguages": learninglanguages}

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AudioListSerializer(
                page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = AudioListSerializer(
            queryset, many=True, context=serializer_context)
        return Response(serializer.data)


@api_view(['POST'])
def audio_togglesaved(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                AudioElement, pk=int(request.data['pk']))
            savings = SavedAudio.objects.filter(audio_element=int(
                request.data['pk']), curator=request.user).first()
            if savings:
               #  print("Element Deleted")
                savings.delete()
                resdata['message'] = "Successfully removed item from saved list"
                resdata['success'] = True
            else:
               #  print("Element Saved")
                savings = SavedAudio.objects.create(
                    audio_element=element, curator=request.user)
                resdata['message'] = "Successfully added item to saved list"
                resdata['success'] = True
        return Response(resdata)


@api_view(['POST'])
def audio_togglehidden(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                AudioElement, pk=int(request.data['pk']))
            if request.user in element.hidden.all():
                element.hidden.remove(request.user)
                element.save()
                resdata['message'] = "Successfully removed item from hidden list"
                resdata['success'] = True
            else:
                element.hidden.add(request.user)
                element.save()
                resdata['message'] = "Successfully added item to hidden list"
                resdata['success'] = True
    return Response(resdata)


@api_view(['POST'])
def audio_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                AudioElement, slug=request.data['slug'])
            if request.data['vote'] == "up":
                resdata['newuservote'] = 1
                if request.user in element.downvote.all():
                    element.downvote.remove(request.user)
                    element.save()
                if request.user not in element.upvote.all():
                    element.upvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully upvoted the audio element!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                resdata['newuservote'] = -1
                if request.user in element.upvote.all():
                    element.upvote.remove(request.user)
                    element.save()
                if request.user not in element.downvote.all():
                    element.downvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully downvoted the audio element!"
                resdata['success'] = True
            resdata['newupcount'] = element.upvote.all().count()
            resdata['newdowncount'] = element.downvote.all().count()

        return Response(resdata)


####### TRANSCRIPT VIEWS ############
class TranscriptViewSet(viewsets.ModelViewSet):
    # queryset = Transcript.objects.all().select_related('curator').prefetch_related('upvote', 'downvote','translations').order_by("-curationdate")
    queryset = Transcript.objects.all().order_by("-curation_date")
    lookup_field = "pk"
    serializer_class = TranscriptSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]


    def retrieve(self, request, pk):
        if request.user.is_authenticated:
            serializer_context = {"request": request}
            queryset = Transcript.objects.all().select_related('curator').order_by("-curation_date")
            transcript = get_object_or_404(queryset, Q(
                published=True) | Q(curator=request.user), pk=pk)
            # transcript = get_object_or_404(Transcript, pk=pk)
            serializer = TranscriptSerializer(
                transcript, context=serializer_context)
            return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        #   print(self.request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        transcript = get_object_or_404(Transcript, pk=pk)
        print("success")
        resdata = {}
        if transcript.curator == request.user:
            serializer_context = {"request": request}
            serializer = TranscriptSerializer(
                transcript, data=request.data, partial=True)
            if serializer.is_valid():
                print("valid")
                serializer.save()
                return Response(serializer.data)
            else:
                print("NOPE")
                resdata['message'] = 'Updates were invalid!'
                resdata['success'] = False
        else:
            resdata['message'] = "You don't have permission!"
            resdata['success'] = False
            #  updatedserializer=AudioElementSerializer(element, context=serializer_context)
        return Response(resdata)


@api_view(['POST'])
def transcript_togglepublish(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(Transcript, pk=int(request.data['pk']))
            if element.curator == request.user:
                if element.published == True:
                    element.published = False
                    element.save()
                    resdata['message'] = "Successfully returned transcript to draft mode"
                    resdata['success'] = True
                    resdata['published'] = element.published
                else:
                    element.published = True
                    element.save()
                    resdata['message'] = "Successfully published transcript."
                    resdata['success'] = True
                    resdata['published'] = element.published
    return Response(resdata)


@api_view(['POST'])
def transcript_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(Transcript, pk=request.data['id'])
            if request.data['vote'] == "up":
                resdata['newuservote'] = 1
                if request.user in element.downvote.all():
                    element.downvote.remove(request.user)
                    element.save()
                if request.user not in element.upvote.all():
                    element.upvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully upvoted the transcript!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                resdata['newuservote'] = -1
                if request.user in element.upvote.all():
                    element.upvote.remove(request.user)
                    element.save()
                if request.user not in element.downvote.all():
                    element.downvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully downvoted the transcript!"
                resdata['success'] = True

            resdata['newupcount'] = element.upvote.all().count()
            resdata['newdowncount'] = element.downvote.all().count()
            # print(resdata)
            return Response(resdata)
        resdata['message'] = "You must be logged in to vote!"
        resdata['success'] = False
        return Response(resdata)


### TRANSLATION VIEWS ###
class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = TranslationSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def retrieve(self, request, pk):
        if request.user.is_authenticated:
            serializer_context = {"request": request}
            translation = get_object_or_404(Translation, pk=pk)
            if translation.published or translation.curator == request.user:
                serializer = TranslationSerializer(
                    translation, context=serializer_context)
                return Response(serializer.data)
            else:
                resdata = {}
                resdata['success'] = False
                resdata['message'] = 'Sorry, but that translation is currently in draft mode and only visible by the author.'
            return Response(resdata)

    def perform_create(self, serializer):
        # After creating a new object, we need to check to see if other translations
        # have already been attached to this transcript by this user...
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        # Determine what to attach the item to:
        if self.request.data['sourcetype']:
            if self.request.data['sourcetype'].lower() == "transcript":
                sourceelement = get_object_or_404(
                    Transcript, pk=self.request.data['sourceid'])
                pass
            elif self.request.data['sourcetype'].lower() == "text":
                sourceelement = get_object_or_404(
                    TextElement, pk=self.request.data['sourceid'])
                pass
            else:
                return Response({"success": "false", "message": "invalid source type"})

            oldtranslation = sourceelement.translations.filter(
                curator=self.request.user)
            if oldtranslation.count() > 0:
                for i in oldtranslation:
                    if i.pk != serializer.data.get('id'):
                        i.delete()
                    print("Deleted old translation")

            # Now we attach the new translation to the transcript
            sourceelement.translations.add(serializer.data['id'])
            sourceelement.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        print("Updating")
        element = get_object_or_404(Translation, pk=pk)
        resdata = {}
        # print(request.data)
        if element.curator == request.user:
            serializer_context = {"request": request}
            serializer = TranslationSerializer(
                element, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                resdata['message'] = 'Translation updated!'
                resdata['success'] = True
            else:
                resdata['message'] = 'Updates were invalid!'
                resdata['success'] = False
        else:
            resdata['message'] = "You don't have permission!"
            resdata['success'] = False
            #  updatedserializer=AudioElementSerializer(element, context=serializer_context)
        return Response(resdata)

    def list(self, request):
        queryset = Translation.objects.filter(
            published=True).order_by("-curationdate")
        serializer_context = {"request": request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TranslationSnippetSerializer(
                page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = TranslationSnippetSerializer(
            queryset, many=True, context=serializer_context)
        return Response(serializer.data)


@api_view(['POST'])
def translation_togglepublish(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                Translation, pk=int(request.data['pk']))
            if element.curator == request.user:
                if element.published == True:
                    element.published = False
                    element.save()
                    resdata['message'] = "Successfully returned translation to draft mode"
                    resdata['success'] = True
                    resdata['published'] = element.published
                else:
                    element.published = True
                    element.save()
                    resdata['message'] = "Successfully published translation."
                    resdata['success'] = True
                    resdata['published'] = element.published
    return Response(resdata)


@api_view(['POST'])
def translation_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(Translation, pk=request.data['id'])
            if request.data['vote'] == "up":
                resdata['newuservote'] = 1
                if request.user in element.downvote.all():
                    element.downvote.remove(request.user)
                    element.save()
                if request.user not in element.upvote.all():
                    element.upvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully upvoted the translation!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                resdata['newuservote'] = -1
                if request.user in element.upvote.all():
                    element.upvote.remove(request.user)
                    element.save()
                if request.user not in element.downvote.all():
                    element.downvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully downvoted the translation!"
                resdata['success'] = True

            resdata['newupcount'] = element.upvote.all().count()
            resdata['newdowncount'] = element.downvote.all().count()
            # print(resdata)
            return Response(resdata)
        resdata['message'] = "You must be logged in to vote!"
        resdata['success'] = False
        return Response(resdata)


### MARKUP VIEWS ###
class MarkupViewSet(viewsets.ModelViewSet):
    queryset = TextMarkup.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = TextMarkupSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def retrieve(self, request, pk):
        if request.user.is_authenticated:
            serializer_context = {"request": request}
            markup = get_object_or_404(TextMarkup, pk=pk)
            if markup.published or markup.curator == request.user:
                serializer = TextMarkupSerializer(
                    markup, context=serializer_context)
                return Response(serializer.data)
            else:
                resdata = {}
                resdata['success'] = False
                resdata['message'] = 'Sorry, but that translation is currently in draft mode and only visible by the author.'
            return Response(resdata)

    def perform_create(self, serializer):
        # After creating a new object, we need to check to see if other translations
        # have already been attached to this transcript by this user..
        serializer_context = {"request": self.request}
        sourcetype = self.request.data.get('sourcetype')
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        print(sourcetype)
        if sourcetype:
            # Determine what to attach the item to:
            sourcetype = sourcetype.lower()
            if sourcetype == "transcript":
                sourceelement = get_object_or_404(
                    Transcript, pk=self.request.data.get('sourceid'))
            elif sourcetype == "textelement":
                sourceelement = get_object_or_404(
                    TextElement, pk=self.request.data.get('sourceid'))
            else:
                return Response({"success": "false", "message": "incorrect source type"})

            oldmarkup = sourceelement.markups.filter(curator=self.request.user)
            if oldmarkup.count() > 0:
                for i in oldmarkup:
                    if i.pk != serializer.data.get('id'):
                        i.delete()
                        print("Deleted old markup")
            else:
                print("no old markups")

            serializer.save(curator=self.request.user, content=sourceelement.content,
                            targetlanguage=self.request.user.user_profile.nativelanguage)
            sourceelement.markups.add(serializer.data['id'])
            sourceelement.save()
        else:
            serializer.save(curator=self.request.user)
        #   return Response(newserializer.data, status=status.HTTP_200_OK)
        #   return newserializer.data

    def partial_update(self, request, pk):
        print("Updating")
        element = get_object_or_404(TextMarkup, pk=pk)
        resdata = {}
        # print(request.data)
        if element.curator == request.user:
            serializer_context = {"request": request}
            serializer = TextMarkupSerializer(
                element, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                resdata['message'] = 'Markup updated!'
                resdata['success'] = True
            else:
                resdata['message'] = 'Updates were invalid!'
                resdata['success'] = False
        else:
            resdata['message'] = "You don't have permission!"
            resdata['success'] = False
            #  updatedserializer=AudioElementSerializer(element, context=serializer_context)
        return Response(resdata)

    def list(self, request):
        #   queryset = TextMarkup.objects.filter(published=False).order_by("-curationdate")
        queryset = TextMarkup.objects.all().order_by("-curationdate")
        serializer_context = {"request": request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TranslationSnippetSerializer(
                page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = TranslationSnippetSerializer(
            queryset, many=True, context=serializer_context)
        return Response(serializer.data)


@api_view(['POST'])
def markup_togglepublish(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(TextMarkup, pk=int(request.data['pk']))
            if element.curator == request.user:
                if element.published == True:
                    element.published = False
                    element.save()
                    resdata['message'] = "Successfully returned markup to draft mode"
                    resdata['success'] = True
                    resdata['published'] = element.published
                else:
                    element.published = True
                    element.save()
                    resdata['message'] = "Successfully published markup."
                    resdata['success'] = True
                    resdata['published'] = element.published
    return Response(resdata)


@api_view(['POST'])
def markup_fork(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            sourcemarkup = get_object_or_404(
                TextMarkup, pk=int(request.data.get('forkparent')))
            source = get_object_or_404(
                TextElement, pk=int(request.data.get('sourceid')))
            newmarkup = TextMarkup()
            newmarkup.content = sourcemarkup.content
            newmarkup.curator = request.user
            newmarkup.forkparent = sourcemarkup
            newmarkup.targetlanguage = request.user.user_profile.nativelanguage
            newmarkup.save()

            oldmarkups = source.markups.filter(curator=request.user)
            if oldmarkups.count() > 0:
                for i in oldmarkups:
                    if i.pk != newmarkup.pk:
                        i.delete()
                        print("Deleted old markup")
                    else:
                        print("Nothing to delete")

            source.markups.add(newmarkup)
            source.save()
            serializer = TextMarkupSerializer(
                newmarkup, context={"request": request})
            print(serializer.data)
            return Response(serializer.data)


@api_view(['POST'])
def markup_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(TextMarkup, pk=request.data['id'])
            if request.data['vote'] == "up":
                resdata['newuservote'] = 1
                if request.user in element.downvote.all():
                    element.downvote.remove(request.user)
                    element.save()
                if request.user not in element.upvote.all():
                    element.upvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully upvoted the markup!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                resdata['newuservote'] = -1
                if request.user in element.upvote.all():
                    element.upvote.remove(request.user)
                    element.save()
                if request.user not in element.downvote.all():
                    element.downvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully downvoted the markup!"
                resdata['success'] = True

            resdata['newupcount'] = element.upvote.all().count()
            resdata['newdowncount'] = element.downvote.all().count()
            # print(resdata)
            return Response(resdata)
        resdata['message'] = "You must be logged in to vote!"
        resdata['success'] = False
        return Response(resdata)


####### TEXT ELEMENT VIEWS ############
class TextViewSet(viewsets.ModelViewSet):
    # queryset = TextElement.objects.all().order_by("-curationdate")
    queryset = TextElement.objects.all().select_related(
        'curator', 'curator__user_profile', 'topic', 'language',
    ).prefetch_related(
        'savedtext_set', 'upvote', 'downvote', 'translations', 'markups', 'flag'
    ).order_by("-curationdate")
    lookup_field = "slug"
    serializer_class = TextElementSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, slug):
        element = get_object_or_404(TextElement, slug=slug)
        serializer_context = {"request": request}
        serializer = TextElementSerializer(
            element, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        updatedserializer = TextElementSerializer(
            element, context=serializer_context)
        return Response(updatedserializer.data)

    def list(self, request):
        learninglanguages = request.user.user_profile.learninglanguage.all()
        user_saved = SavedText.objects.filter(curator=request.user)
        queryset = TextElement.objects.filter(
            suspended=False,
        ).select_related(
            'curator', 'curator__user_profile', 'language', 'topic',
        ).prefetch_related(
            'translations', 'hidden', 'upvote', 'downvote', 'flag',
        ).prefetch_related(
            Prefetch('savedtext_set', queryset=user_saved)
        ).order_by("-curationdate")

        serializer_context = {
            "request": request, "learninglanguages": learninglanguages}

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TextListSerializer(
                page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)

        serializer = TextListSerializer(
            queryset, many=True, context=serializer_context)
        return Response(serializer.data)


@api_view(['POST'])
def text_togglesaved(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                TextElement, pk=int(request.data['pk']))
            savings = SavedText.objects.filter(text_element=int(
                request.data['pk']), curator=request.user).first()
            if savings:
                print("Element Deleted")
                savings.delete()
                resdata['message'] = "Successfully removed item from saved list"
                resdata['success'] = True
            else:
                print("Element Saved")
                savings = SavedText.objects.create(
                    text_element=element, curator=request.user)
                resdata['message'] = "Successfully added item to saved list"
                resdata['success'] = True
        return Response(resdata)


@api_view(['POST'])
def text_togglehidden(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                TextElement, pk=int(request.data['pk']))
            if request.user in element.hidden.all():
                element.hidden.remove(request.user)
                element.save()
                resdata['message'] = "Successfully removed item from hidden list"
                resdata['success'] = True
            else:
                element.hidden.add(request.user)
                element.save()
                resdata['message'] = "Successfully added item to hidden list"
                resdata['success'] = True
    return Response(resdata)


@api_view(['POST'])
def text_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(TextElement, slug=request.data['slug'])
            if request.data['vote'] == "up":
                resdata['newuservote'] = 1
                if request.user in element.downvote.all():
                    element.downvote.remove(request.user)
                    element.save()
                if request.user not in element.upvote.all():
                    element.upvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully upvoted the text element!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                resdata['newuservote'] = -1
                if request.user in element.upvote.all():
                    element.upvote.remove(request.user)
                    element.save()
                if request.user not in element.downvote.all():
                    element.downvote.add(request.user)
                    element.save()
                resdata['message'] = "Successfully downvoted the text element!"
                resdata['success'] = True
            resdata['newupcount'] = element.upvote.all().count()
            resdata['newdowncount'] = element.downvote.all().count()

        return Response(resdata)

