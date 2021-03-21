from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, action
from django.db.models import Prefetch, Q, Exists, OuterRef, Count
from django_filters.rest_framework import DjangoFilterBackend
import django_filters as django_filter

from vocab.models import  (
                        WordRoot, 
                        Lexeme,
                        LexemeGrammar,
                        LexemeDefinition,
                        LexemePronunciation,
                        LexemeRoot,
                        LexemePairLearning,
                        InflectedForm,
                        InflectedFormGrammar,
                        InflectedFormDefinition,
                        InflectedFormPronunciation,
                        InflectedFormImage,
                        Sentence,
                        InflectedFormSentence,
                        SentenceTranslation,
                        SentenceAudio,
                        LexemePair,
                        InflectedFormPair,
                        VocabBank,
                        CardStack,
                        FavoriteStack,
                        )
from categories.models import Language
from lessons.models import LessonVocabBank

from vocab.api.serializers import (
                           LexemeSerializer,
                           LexemeDefinitionSerializer,
                           LexemePronunciationSerializer,
                           VocabBankSerializer,
                           SentenceSerializer,
                           SentenceAudioSerializer,
                           SentenceTranslationSerializer,
                           InflectedFormSentenceSerializer,
                           InflectedFormSerializer,
                           InflectedFormDefinitionSerializer,
                           InflectedFormPronunciationSerializer,
                           InflectedFormPairSerializer,
                           CardStackSerializer,
                           QuickStackSerializer,
                           LearnStackSerializer,
                           LexemePairSerializer,
                           FavoriteStackSerializer,
                            )
from rest_framework.permissions import IsAuthenticated, IsAdminUser


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


class CardStackFilter(django_filter.FilterSet):
    tags = django_filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CardStack
        fields = ('curator__username',)


class CardStackList(generics.ListAPIView):
    model = CardStack
    serializer_class = QuickStackSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CardStackFilter
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['name', 'learning_language'
                       'curationdate', 'updated', 'native_language']
    ordering = ['-curationdate']

    def get_queryset(self):
        user = self.request.user
        queryset = CardStack.objects.filter(public=True).select_related(
            'curator__user_profile', 'native_language', 'learning_language'
        ).prefetch_related(
            'saves',
        ).annotate(
            user_has_saved=Exists(
                FavoriteStack.objects.filter(
                    stack=OuterRef('pk'),
                    user=user
                ))
        ).order_by('-curationdate')
        by_preference = self.request.query_params.get('by_preference', None)
        by_saves = self.request.query_params.get('saved', None)
        if by_preference is not None:
            queryset = queryset.filter(learning_language__in=user.user_profile.learninglanguage.all())
        if by_saves is not None:
            queryset = queryset.filter(saves__user=user).order_by('-saves__created')
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET'])
def get_word_list(request):
   resdata = {}
   if request.method == 'GET':
      language_param = request.GET.get('language', '')
      if language_param == '':
         words = InflectedForm.objects.filter(language = None).order_by("-word")
      elif language_param == 'all':
         words = InflectedForm.objects.all().order_by("-word")
      else:
         language = get_object_or_404(Language, name=language_param)
         words = InflectedForm.objects.filter(language = language)

      return Response(InflectedFormSerializer(words, many=True).data)
   return Response(resdata)





@api_view(['GET'])
def get_lexeme_list(request):
   resdata = {}
   if request.method == 'GET':
      language_param = request.GET.get('language', '')
      if language_param == '':
         words = Lexeme.objects.filter(language = None).order_by("-lemma")
      elif language_param == 'all':
         words = Lexeme.objects.all().order_by("-lemma")
      else:
         language = get_object_or_404(Language, name=language_param)
         words = Lexeme.objects.filter(language = language)

      return Response(LexemeSerializer(words, many=True).data)
   return Response(resdata)


#### INFLECTED FORMS #######
class InflectedFormViewSet(viewsets.ModelViewSet):

    queryset = InflectedForm.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = InflectedFormSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        lexeme_id=self.request.data.get('lexeme_id')
        lexeme_slug=self.request.data.get('lexemeslug')
        if lexeme_id:
            lexeme = get_object_or_404(Lexeme, pk=lexeme_id)
            serializer.save(curator=self.request.user, lexeme=lexeme)
        elif lexeme_slug:
            lexeme = get_object_or_404(Lexeme, slug=lexeme_slug)
            serializer.save(curator=self.request.user, lexeme=lexeme)
        else:
            serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 3
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# This view is specific to sorting, counting, and displaying a list to the user when creating a new group
@api_view(['GET'])
def wordpair_list(request, pk):
   wordpairs = InflectedFormPair.objects.filter(
                              Q(inflected_form_1 = pk) | Q(inflected_form_2 = pk)
                              )
   wordlist = {}
   for pair in wordpairs:
      if pair.inflected_form_1 != pk:
            if pair.inflected_form_1.pk in wordlist.keys():
               wordlist[pair.inflected_form_1.pk] += 1
            else:
               wordlist[pair.inflected_form_1.pk] = 1
      else:
            if pair.inflected_form_2.pk in wordlist.keys():
               wordlist[pair.inflected_form_2.pk] += 1
            else:
               wordlist[pair.inflected_form_2.pk] = 1

   resdata = []
   for key in wordlist:
      associated_word = get_object_or_404(InflectedForm, pk=key)
      word_object = InflectedFormSerializer(associated_word)
      word_package = {
         'id': associated_word.pk,
         'lexeme': associated_word.lexeme.lemma,
         'count': wordlist[key],
         'word': associated_word.word,
         'language': associated_word.language,
      }
      resdata.append(word_package)

   # return InflectedFormSerializer(wordlist.keys(), many=True).data
   return Response(resdata)


@api_view(['POST'])
def remove_pair_from_bank(request):
   if request.user.is_authenticated:
      vocab_bank = get_object_or_404(VocabBank, pk=request.data.get('vocab_bank'))
      if vocab_bank.curator != request.user:
         return Response(status=status.HTTP_401_UNAUTHORIZED)
      else:
         word_pair = get_object_or_404(InflectedFormPair, pk=request.data.get('word_pair'))
         vocab_bank.word_pairs.remove(word_pair)

         return Response(status=status.HTTP_202_ACCEPTED)



@api_view(['POST'])
def add_pair_to_vocab_bank(request):
   if request.user.is_authenticated:
      vocab_bank = get_object_or_404(VocabBank, pk=request.data.get('vocab_bank'))
      if vocab_bank.curator != request.user:
         return Response(status=status.HTTP_401_UNAUTHORIZED)
      else:
         word1 = get_object_or_404(InflectedForm, pk=request.data.get('inflected_form_1'))
         word2 = get_object_or_404(InflectedForm, pk=request.data.get('inflected_form_2'))

         queryset = InflectedFormPair.objects.filter(
                                    (Q(inflected_form_1 = word1) & Q(inflected_form_2 = word2)) |
                                    (Q(inflected_form_1 = word2) & Q(inflected_form_2 = word1)),
                                    curator = request.user
                                    ).order_by("-curationdate")
         # ensure pairing doesn't exist in Bank
         if queryset.count() > 0:
            pairing = queryset[0]
            # add pairing to Bank....
            vocab_bank.word_pairs.add(pairing)
            vocab_bank.save()

            request.user.user_profile.points += 1
            request.user.user_profile.save()

            # return pairing back to user for display in vocab bank
            resdata = InflectedFormPairSerializer(pairing).data
            return Response(resdata)
         else:
            # create new pairing
            pairing=InflectedFormPair()
            
            pairing.curator = request.user
            pairing.inflected_form_1 = word1
            pairing.inflected_form_2 = word2
            pairing.curator_note = request.data.get('curator_note')
            
            pairing.save()

            # add pairing to Bank....
            vocab_bank.word_pairs.add(pairing)
            vocab_bank.save()

            # give user 2 points; 1 for a new pairing, and 1 for addding the pair to the bank
            request.user.user_profile.points += 2
            request.user.user_profile.save()

            # return new pairing back to user for display in vocab bank
            resdata = InflectedFormPairSerializer(pairing).data
            return Response(resdata)


class InflectedFormPairViewSet(viewsets.ModelViewSet):
   queryset = InflectedFormPair.objects.all().order_by("-curationdate")
   lookup_field = "pk"
   serializer_class = InflectedFormPairSerializer
   permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]
    
   def get_serializer_context(self):
      """
      pass request attribute to serializer
      """
      context = super(InflectedFormPairViewSet, self).get_serializer_context()
      context.update({"request": self.request})
      return context    

   def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)

      word1 = self.request.data['inflected_form_1']
      word2 = self.request.data['inflected_form_2']

      queryset = InflectedFormPair.objects.filter(
                                 (Q(inflected_form_1 = word1) & Q(inflected_form_2 = word2)) |
                                 (Q(inflected_form_1 = word2) & Q(inflected_form_2 = word1)),
                                 curator = self.request.user
                                 ).order_by("-curationdate")
      if queryset.count() > 0:
         # return Response({"message":"Sorry, Charlie"}, status=status.HTTP_406_NOT_ACCEPTABLE)
         resdata = InflectedFormPairSerializer(queryset[1]).data
         return Response(resdata)
      else:
         self.perform_create(serializer)
         headers = self.get_success_headers(serializer.data)
         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


   def perform_create(self, serializer):
      # Check to see if user already has a pair:
      serializer.save(curator=self.request.user)
      self.request.user.user_profile.points += 2
      self.request.user.user_profile.save()






###### LEXEME VIEWS #######
class LexemeViewSet(viewsets.ModelViewSet):

    queryset = Lexeme.objects.all().order_by("-curationdate")
    lookup_field = "slug"
    serializer_class = LexemeSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 5
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # This list is currently factoring in user preferences and filtering by learning languages/topics
    def list(self, request):
      userlanguages = request.user.user_profile.learninglanguage.all()
      queryset = Lexeme.objects.all().order_by("-curationdate")
      # queryset = Lexeme.objects.filter(
      #    suspended = False,
      # #   language__in = userlanguages,
      # ).order_by("-curationdate")

      serializer_context = {"request": request, "userlanguages": userlanguages}
      
      page = self.paginate_queryset(queryset)
      if page is not None:
         serializer = LexemeSerializer(page, many=True, context=serializer_context) 
         return self.get_paginated_response(serializer.data)

      serializer = LexemeSerializer(queryset, many=True, context=serializer_context) 
      return Response(serializer.data)

class LexemeDefinitionViewSet(viewsets.ModelViewSet):
    queryset = LexemeDefinition.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = LexemeDefinitionSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # This list is currently factoring in user preferences and filtering by learning languages/topics
    def list(self, request):
      userlanguages = request.user.user_profile.learninglanguage.all()
      queryset = LexemeDefinition.objects.all().order_by("-curationdate")
      # queryset = Lexeme.objects.filter(
      #    suspended = False,
      # #   language__in = userlanguages,
      # #   topic__in = usertopics,
      # ).order_by("-curationdate")

      serializer_context = {"request": request, "userlanguages": userlanguages}
      
      page = self.paginate_queryset(queryset)
      if page is not None:
         serializer = LexemeDefinitionSerializer(page, many=True, context=serializer_context) 
         return self.get_paginated_response(serializer.data)

      serializer = LexemeDefinitionSerializer(queryset, many=True, context=serializer_context) 
      return Response(serializer.data)

class SentenceViewSet(viewsets.ModelViewSet):
    queryset = Sentence.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = SentenceSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_sentence_search(request, pk):
   word = get_object_or_404(InflectedForm, pk=pk);
   if word.pk:
      sentences = Sentence.objects.filter(
                  language=word.language, text__contains=word.word
               )
      serializer = SentenceSerializer(sentences, many=True)
      return Response(serializer.data)
   return Response(status=status.HTTP_404_NOT_FOUND)

class InflectedSentenceViewSet(viewsets.ModelViewSet):
    queryset = InflectedFormSentence.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = InflectedFormSentenceSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class InflectedFormDefinitionViewSet(viewsets.ModelViewSet):
    queryset = InflectedFormDefinition.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = InflectedFormDefinitionSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # This list is currently factoring in user preferences and filtering by learning languages/topics
    def list(self, request):
      userlanguages = request.user.user_profile.learninglanguage.all()
      queryset = InflectedFormDefinition.objects.all().order_by("-curationdate")
      # queryset = Lexeme.objects.filter(
      #    suspended = False,
      # #   language__in = userlanguages,
      # #   topic__in = usertopics,
      # ).order_by("-curationdate")

      serializer_context = {"request": request, "userlanguages": userlanguages}
      
      page = self.paginate_queryset(queryset)
      if page is not None:
         serializer = InflectedFormDefinitionSerializer(page, many=True, context=serializer_context) 
         return self.get_paginated_response(serializer.data)

      serializer = InflectedFormDefinitionSerializer(queryset, many=True, context=serializer_context) 
      return Response(serializer.data)


@api_view(['GET'])
def lexeme_definition_list(request, slug):
   lexeme = get_object_or_404(Lexeme, slug=slug);
   definitions = lexeme.lexemedefinition_set.all()
   serializer = LexemeDefinitionSerializer(definitions, many=True)
   return Response(serializer.data)

@api_view(['GET'])
def lexeme_word_list(request, slug):
   lexeme = get_object_or_404(Lexeme, slug=slug);
   words = lexeme.inflectedform_set.all()
   serializer = InflectedFormSerializer(words, many=True)
   return Response(serializer.data)
   # resdata = {}
   # if request.method == 'GET':
   #    language_param = request.GET.get('language', '')
   #    if language_param == '':
   #       words = InflectedForm.objects.filter(language = None).order_by("-word")
   #    elif language_param == 'all':
   #       words = InflectedForm.objects.all().order_by("-word")
   #    else:
   #       language = get_object_or_404(Language, name=language_param)
   #       words = InflectedForm.objects.filter(language = language)

   #    return Response(InflectedFormSerializer(words, many=True).data)
   # return Response(resdata)


class LexemePronunciationViewSet(viewsets.ModelViewSet):
    queryset = LexemePronunciation.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = LexemePronunciationSerializer
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, slug):
       pronunciation = get_object_or_404(LexemePronunciation, pk=id)
       serializer_context = {"request": request}
       serializer=LexemePronunciationSerializer(pronunciation, data=request.data, partial=True)
       if serializer.is_valid():
         serializer.save()
       updatedserializer=LexemePronunciationSerializer(pronunciation, context=serializer_context)
       return Response(updatedserializer.data)


    # This list is currently factoring in user preferences and filtering by learning languages/topics
    def list(self, request):
      userlanguages = request.user.user_profile.learninglanguage.all()
      queryset = LexemePronunciation.objects.all().order_by("-curationdate")
      # queryset = Lexeme.objects.filter(
      #    suspended = False,
      # #   language__in = userlanguages,
      # #   topic__in = usertopics,
      # ).order_by("-curationdate")

      serializer_context = {"request": request, "userlanguages": userlanguages}
      
      page = self.paginate_queryset(queryset)
      if page is not None:
         serializer = LexemePronunciationSerializer(page, many=True, context=serializer_context) 
         return self.get_paginated_response(serializer.data)

      serializer = LexemePronunciationSerializer(queryset, many=True, context=serializer_context) 
      return Response(serializer.data)


@api_view(['GET'])
def lexeme_pronunciation_list(request, slug):
   lexeme = get_object_or_404(Lexeme, slug=slug);
   pronunciations = lexeme.lexemepronunciation_set.all()
   serializer = LexemePronunciationSerializer(pronunciations, many=True)
   return Response(serializer.data)


class InflectedFormPronunciationViewSet(viewsets.ModelViewSet):
    queryset = InflectedFormPronunciation.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = InflectedFormPronunciationSerializer
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, slug):
       pronunciation = get_object_or_404(InflectedFormPronunciation, pk=id)
       serializer_context = {"request": request}
       serializer=InflectedFormPronunciationSerializer(pronunciation, data=request.data, partial=True)
       if serializer.is_valid():
         serializer.save()
       updatedserializer=InflectedFormPronunciationSerializer(pronunciation, context=serializer_context)
       return Response(updatedserializer.data)

@api_view(['GET'])
def inflected_form_pronunciation_list(request, pk):
   inflected_form = get_object_or_404(InflectedForm, pk=pk);
   pronunciations = inflected_form.inflectedformpronunciation_set.all()
   serializer = InflectedFormPronunciationSerializer(pronunciations, many=True)
   return Response(serializer.data)


###### VOCAB BANK VIEWS #######
class VocabBankViewSet(viewsets.ModelViewSet):

    queryset = VocabBank.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = VocabBankSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 5
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SentenceAudioViewSet(viewsets.ModelViewSet):
    queryset = SentenceAudio.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = SentenceAudioSerializer
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):

        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    def partial_update(self, request, pk):
       audio = get_object_or_404(SentenceAudio, pk=pk)
       serializer_context = {"request": request}
       serializer=SentenceAudioSerializer(audio, data=request.data, partial=True)
       if serializer.is_valid():
         serializer.save()
       updatedserializer=SentenceAudioSerializer(audio, context=serializer_context)
       return Response(updatedserializer.data)


class SentenceTranslationViewSet(viewsets.ModelViewSet):
    queryset = SentenceTranslation.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = SentenceTranslationSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class CardStackViewSet(viewsets.ModelViewSet):
   queryset = CardStack.objects.filter().select_related(
      'curator', 'learning_language', 'native_language'
   ).prefetch_related(
      'lexeme_pairs'
   ).order_by("-curationdate")
   lookup_field = "slug"
   serializer_class = CardStackSerializer
   permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

   def list(self, request):
      queryset = CardStack.objects.filter(
                                 Q(public = True) | Q(curator = request.user)
                              ).order_by("-curationdate")
      context = {
         'request':request
      }
      serializer = QuickStackSerializer(queryset, many=True, context=context) 
      return Response(serializer.data)

   def perform_create(self, serializer):
      serializer.save(curator=self.request.user)
      self.request.user.user_profile.points += 2
      self.request.user.user_profile.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

   def partial_update(self, request, slug):
      stack = get_object_or_404(CardStack, slug=slug)
      # serializer_context = {"request": request}
      serializer=CardStackSerializer(stack, data=request.data, partial=True)
      if serializer.is_valid():
         serializer.save()
         # updatedserializer=CardStackSerializer(stack)
      return Response(serializer.data)


@api_view(['GET'])
def learn_stack_view(request, slug):
   stack = get_object_or_404(CardStack, slug=slug)
   # print(request)
   serializer = LearnStackSerializer(stack, context={'request': request})
   return Response(serializer.data)
   


class LearnStackViewSet(viewsets.ModelViewSet):
   queryset = CardStack.objects.all().order_by("-curationdate")
   lookup_field = "slug"
   serializer_class = LearnStackSerializer
   permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

   def list(self, request):
      # userlanguages = request.user.user_profile.learninglanguage.all()
      # usertopics = request.user.user_profile.learningtopics.all()
      queryset = CardStack.objects.filter(
                                 Q(public = True) | Q(curator = request.user)
                              ).order_by("-curationdate")
      # queryset = Lexeme.objects.filter(
      #    suspended = False,
      # #   language__in = userlanguages,
      # #   topic__in = usertopics,
      # ).order_by("-curationdate")

      # serializer_context = {"request": request, "userlanguages": userlanguages, "usertopics": usertopics}
      
      # page = self.paginate_queryset(queryset)
      # if page is not None:
      #    serializer = LexemeSerializer(page, many=True, context=serializer_context) 
      #    return self.get_paginated_response(serializer.data)

      serializer = LearnStackSerializer(queryset, many=True) 
      return Response(serializer.data)



@api_view(['POST'])
def add_stack_pair(request):
   if request.user.is_authenticated:
      stack = get_object_or_404(CardStack, slug=request.data.get('stack'))
      if stack.curator != request.user:
         return Response(status=status.HTTP_401_UNAUTHORIZED)
      pair = get_object_or_404(LexemePair, pk=request.data.get('pair'))
      stack.lexeme_pairs.add(pair)
      stack.save()
      resdata = LexemePairSerializer(pair).data
      return Response(resdata)

@api_view(['POST'])
def delete_stack_pair(request):
   if request.user.is_authenticated:
      stack = get_object_or_404(CardStack, slug=request.data.get('stack'))
      if stack.curator != request.user:
         return Response(status=status.HTTP_401_UNAUTHORIZED)
      pair = get_object_or_404(LexemePair, pk=request.data.get('pair'))
      stack.lexeme_pairs.remove(pair)
      stack.save()
      resdata = {}
      resdata['message'] = 'Pairing removed'
      return Response(resdata)

class FavoriteStackViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return FavoriteStack.objects.filter(curator=self.request.user).select_related('stack').order_by("-stack")

   #  queryset = FavoriteStack.objects.filter(curator=request.user).order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = FavoriteStackSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]
   #  serializer=LexemePronunciationSerializer(pronunciation, data=request.data, partial=True)

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def stack_togglesave(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            try: 
                stack = get_object_or_404(CardStack, slug=request.data['slug'])
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                saved = FavoriteStack.objects.filter(user=request.user,stack=stack)
                if saved:
                    saved.delete()
                    resdata['message'] = "Successfully removed item from saved list"
                    resdata['success'] = True
                    resdata['saved'] = False
                else:
                    FavoriteStack.objects.create(user=request.user, stack=stack)
                    resdata['message'] = "Successfully added item to saved list"
                    resdata['success'] = True
                    resdata['saved'] = True
    return Response(resdata)

class LexemePronunciationViewSet(viewsets.ModelViewSet):
    queryset = LexemePronunciation.objects.all().order_by("-curationdate")
    lookup_field = "pk"
    serializer_class = LexemePronunciationSerializer
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
       pronunciation = get_object_or_404(LexemePronunciation, pk=pk)
       serializer_context = {"request": request}
       serializer=LexemePronunciationSerializer(pronunciation, data=request.data, partial=True)
       if serializer.is_valid():
         serializer.save()
       updatedserializer=LexemePronunciationSerializer(pronunciation, context=serializer_context)
       return Response(updatedserializer.data)


class LexemePairViewSet(viewsets.ModelViewSet):
    queryset = LexemePair.objects.all().order_by("-curationdate")
   #  lookup_field = "slug"
    serializer_class = LexemePairSerializer
    permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save(curator=self.request.user)
        self.request.user.user_profile.points += 2
        self.request.user.user_profile.save()


@api_view(['GET'])
def get_lexemepair_list(request, slug, pairlanguage):
   lexeme = get_object_or_404(Lexeme, slug=slug)
   lexemepairs = LexemePair.objects.filter(
                              Q(lexeme_1 = lexeme) | Q(lexeme_2 = lexeme)
                              )

   # language_param = request.GET.get('language', '')

   if pairlanguage:
      language = get_object_or_404(Language, name=pairlanguage)
      newPairSet = []
      for i in lexemepairs:
         newPair = {}
         if i.lexeme_1 != lexeme:
            l1 = i.lexeme_1
            if l1.language == language:
               newPair['id']=i.id
               serializer = LexemeSerializer(l1)
               newPair['pairing']=serializer.data
               newPairSet.append(newPair)
         else:
            l2 = i.lexeme_2
            if l2.language == language:
               newPair['id']=i.id
               serializer = LexemeSerializer(l2)
               newPair['pairing']=serializer.data
               newPairSet.append(newPair)

      return Response(newPairSet)
   serializer = LexemePairSerializer(lexemepairs, many=True)
   return Response(serializer.data)


@api_view(['GET'])
def get_word_list(request):
   resdata = {}
   if request.method == 'GET':
      language_param = request.GET.get('language', '')
      if language_param == '':
         words = InflectedForm.objects.filter(language = None).order_by("-word")
      elif language_param == 'all':
         words = InflectedForm.objects.all().order_by("-word")
      else:
         language = get_object_or_404(Language, name=language_param)
         words = InflectedForm.objects.filter(language = language)

      return Response(InflectedFormSerializer(words, many=True).data)
   return Response(resdata)



@api_view(['POST'])
def update_lexeme_learning_correct(request):
   if request.user.is_authenticated:
      print(request.data)
      learning_pair = get_object_or_404(LexemePairLearning, pk=request.data.get('learning_pair_id'))
      if learning_pair.curator != request.user:
         return Response(status=status.HTTP_401_UNAUTHORIZED)
      else:
         learning_pair.attempts = learning_pair.attempts + 1
         learning_pair.number_correct = learning_pair.number_correct + 1
         learning_pair.save()
         return Response({'message': 'Correct answer recorded'})

@api_view(['POST'])
def update_lexeme_learning_incorrect(request):
   if request.user.is_authenticated:
      print(request.data)
      learning_pair = get_object_or_404(LexemePairLearning, pk=request.data.get('learning_pair_id'))
      if learning_pair.curator != request.user:
         return Response(status=status.HTTP_401_UNAUTHORIZED)
      else:
         learning_pair.attempts = learning_pair.attempts + 1
         learning_pair.save()
         return Response({'message': 'Incorrect answer recorded'})
