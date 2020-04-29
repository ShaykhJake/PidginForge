from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, action

from elements.api.serializers import (
                           YouTubeElementSerializer,
                           AudioElementSerializer,
                           TextElementSerializer,
                           TranscriptSerializer,
                           TranscriptSnippetSerializer,
                           TranslationSerializer,
                           TranslationSnippetSerializer,
                           TextMarkupSerializer,
                           MarkupSnippetSerializer,
                            )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from elements.models import (
                           YouTubeElement, 
                           Transcript, 
                           Translation, 
                           AudioElement, 
                           TextElement,
                           TextMarkup
                           )


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


###### YOUTUBE ELEMENT VIEWS #######
class YouTubeViewSet(viewsets.ModelViewSet):

    queryset = YouTubeElement.objects.all().order_by("-curationdate")
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
        userlanguages = request.user.user_profile.learninglanguage.all()
        usertopics = request.user.user_profile.learningtopics.all()

        queryset = YouTubeElement.objects.filter(
           suspended = False,
         #   language__in = userlanguages,
         #   topic__in = usertopics,
        ).order_by("-curationdate")

        serializer_context = {"request": request, "userlanguages": userlanguages, "usertopics": usertopics}
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = YouTubeElementSerializer(page, many=True, context=serializer_context) 
            return self.get_paginated_response(serializer.data)

        serializer = YouTubeElementSerializer(queryset, many=True, context=serializer_context) 
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


@api_view(['POST'])
def youtube_togglesaved(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         element = get_object_or_404(YouTubeElement, pk=int(request.data['pk']))
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
def youtube_togglehidden(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         element = get_object_or_404(YouTubeElement, pk=int(request.data['pk']))
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
         element = get_object_or_404(YouTubeElement, slug=request.data['slug'])
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
      # kwarg_slug = request.kwargs.get("slug")
      youtube = YouTubeElement.objects.get(slug=slug)

      serializer = YouTubeElementSerializer(youtube)
      # if serializer.is_valid():
      #    print("HELLO!")
      resdata = {}
      resdata['message'] = "Hi there"
      resdata['available'] = True
      # if serializer.is_valid():
      #    resdata['response'] = "successfully registered a new user."
      #    resdata['email'] = account.email
      # else:
      #    data = serializer.errors
      #    # data = serializer.data
      return Response(resdata)
      # return Response(youtube)
      # return True

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

    queryset = AudioElement.objects.all().order_by("-curationdate")
    lookup_field = "slug"
    serializer_class = AudioElementSerializer
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

   #  def create(self, request):
   #     print(request.data['audiofile'])
   #     resdata = {}
   #     resdata["message"]="hello"
   #     return Response(resdata)

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, slug):
       element = get_object_or_404(AudioElement, slug=slug)
       serializer_context = {"request": request}
       serializer=AudioElementSerializer(element, data=request.data, partial=True)
       if serializer.is_valid():
         serializer.save()
       updatedserializer=AudioElementSerializer(element, context=serializer_context)
       return Response(updatedserializer.data)

    # This list is currently factoring in user preferences and filtering by learning languages/topics
    def list(self, request):
      #   userlanguages = request.user.user_profile.learninglanguage.all()
      #   usertopics = request.user.user_profile.learningtopics.all()
        queryset = AudioElement.objects.filter(
           suspended = False,
         #   language__in = userlanguages,
         #   topic__in = usertopics,
        ).order_by("-curationdate")

        serializer_context = {"request": request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AudioElementSerializer(page, many=True, context=serializer_context) 
            return self.get_paginated_response(serializer.data)

        serializer = AudioElementSerializer(queryset, many=True, context=serializer_context) 
        return Response(serializer.data)


@api_view(['POST'])
def audio_togglesaved(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         element = get_object_or_404(AudioElement, pk=int(request.data['pk']))
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
def audio_togglehidden(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         element = get_object_or_404(AudioElement, pk=int(request.data['pk']))
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
         element = get_object_or_404(AudioElement, slug=request.data['slug'])
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
    queryset = Transcript.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = TranscriptSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

   #  def create(self, request):
   #     print(request.data['audiofile'])
   #     resdata = {}
   #     resdata["message"]="hello"
   #     return Response(resdata)
    def retrieve(self, request, pk):
       if request.user.is_authenticated:
         serializer_context = {"request": request}
         transcript = get_object_or_404(Transcript, pk=pk)
         if transcript.published or transcript.curator == request.user:
            serializer=TranscriptSerializer(transcript, context=serializer_context)
            return Response(serializer.data)
         else:
            resdata = {}
            resdata['success']=False
            resdata['message']='Sorry, but that transcript is currently in draft mode and only visible by the author.'
         return Response(resdata)


    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
      #   print(self.request.data)
        if self.request.data['elementtype']=='YouTube':
           element = get_object_or_404(YouTubeElement, slug=self.request.data['elementslug']) 

        elif self.request.data['elementtype']=='Audio':
           element = get_object_or_404(AudioElement, slug=self.request.data['elementslug'])
        
        if self.request.data['usertranscript']:
           print("Yup, user script exists")
           userscript = get_object_or_404(Transcript, pk=self.request.data['usertranscript'])
           if userscript:
              print("Userscript deleted")
              userscript.delete()
            #   element.transcripts.remove(userscript)
            #   element.save()

        element.transcripts.add(serializer.data['id'])
        element.save()
      
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
      print("Updating")
      element = get_object_or_404(Transcript, pk=pk)
      resdata = {}
      if element.curator == request.user:
         serializer_context = {"request": request}
         serializer=TranscriptSerializer(element, data=request.data, partial=True)
         if serializer.is_valid():
            serializer.save()
            resdata['message'] = 'Transcript updated!'
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
        queryset = Transcript.objects.filter(published=True).order_by("-curationdate")
        serializer_context = {"request": request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TranscriptSnippetSerializer(page, many=True, context=serializer_context) 
            return self.get_paginated_response(serializer.data)

        serializer=TranscriptSnippetSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

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
            serializer=TranslationSerializer(translation, context=serializer_context)
            return Response(serializer.data)
         else:
            resdata = {}
            resdata['success']=False
            resdata['message']='Sorry, but that translation is currently in draft mode and only visible by the author.'
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
            sourceelement = get_object_or_404(Transcript, pk=self.request.data['sourceid'])
            pass
         elif self.request.data['sourcetype'].lower() == "text":
            sourceelement = get_object_or_404(TextElement, pk=self.request.data['sourceid'])
            pass
         else:
            return Response({"success":"false","message":"invalid source type"})

         oldtranslation = sourceelement.translations.filter(curator=self.request.user)
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
         serializer=TranslationSerializer(element, data=request.data, partial=True)
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
        queryset = Translation.objects.filter(published=True).order_by("-curationdate")
        serializer_context = {"request": request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TranslationSnippetSerializer(page, many=True, context=serializer_context) 
            return self.get_paginated_response(serializer.data)

        serializer=TranslationSnippetSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

@api_view(['POST'])
def translation_togglepublish(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         element = get_object_or_404(Translation, pk=int(request.data['pk']))
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
            serializer=TextMarkupSerializer(markup, context=serializer_context)
            return Response(serializer.data)
         else:
            resdata = {}
            resdata['success']=False
            resdata['message']='Sorry, but that translation is currently in draft mode and only visible by the author.'
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
               sourceelement = get_object_or_404(Transcript, pk=self.request.data.get('sourceid'))
            elif sourcetype == "textelement":
               sourceelement = get_object_or_404(TextElement, pk=self.request.data.get('sourceid'))
            else:
               return Response({"success":"false","message":"incorrect source type"})

            oldmarkup = sourceelement.markups.filter(curator=self.request.user)
            if oldmarkup.count() > 0:
               for i in oldmarkup:
                  if i.pk != serializer.data.get('id'):
                     i.delete()
                     print("Deleted old markup")
            else:
               print("no old markups")
            
            serializer.save(curator=self.request.user, content=sourceelement.content, targetlanguage=self.request.user.user_profile.nativelanguage)
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
         serializer=TextMarkupSerializer(element, data=request.data, partial=True)
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
            serializer = TranslationSnippetSerializer(page, many=True, context=serializer_context) 
            return self.get_paginated_response(serializer.data)

        serializer=TranslationSnippetSerializer(queryset, many=True, context=serializer_context)
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
         sourcemarkup = get_object_or_404(TextMarkup, pk=int(request.data.get('forkparent')))
         source = get_object_or_404(TextElement, pk=int(request.data.get('sourceid')))
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
         serializer = TextMarkupSerializer(newmarkup, context={"request": request})
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
    queryset = TextElement.objects.all().order_by("-curationdate")
    lookup_field = "slug"
    serializer_class = TextElementSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

   #  def create(self, request):
   #     print(request.data['audiofile'])
   #     resdata = {}
   #     resdata["message"]="hello"
   #     return Response(resdata)

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, slug):
       element = get_object_or_404(TextElement, slug=slug)
       serializer_context = {"request": request}
       serializer=TextElementSerializer(element, data=request.data, partial=True)
       if serializer.is_valid():
         serializer.save()
         print('yep')
       else:
         print("nope")
       updatedserializer=TextElementSerializer(element, context=serializer_context)
       return Response(updatedserializer.data)

    def list(self, request):
      #   userlanguages = request.user.user_profile.learninglanguage.all()
      #   usertopics = request.user.user_profile.learningtopics.all()
        queryset = TextElement.objects.filter(
           suspended = False,
         #   language__in = userlanguages,
         #   topic__in = usertopics,
        ).order_by("-curationdate")

        serializer_context = {"request": request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TextElementSerializer(page, many=True, context=serializer_context) 
            return self.get_paginated_response(serializer.data)

        serializer = TextElementSerializer(queryset, many=True, context=serializer_context) 
        return Response(serializer.data)


@api_view(['POST'])
def text_togglesaved(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         element = get_object_or_404(TextElement, pk=int(request.data['pk']))
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
def text_togglehidden(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         element = get_object_or_404(TextElement, pk=int(request.data['pk']))
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


