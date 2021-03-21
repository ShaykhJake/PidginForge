from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, action
from django.db.models import Prefetch, Q, Exists, OuterRef, Count
from django_filters.rest_framework import DjangoFilterBackend
import django_filters as django_filter
from lessons.api.serializers import (
                           LessonSerializer,
                           LessonVocabBankSerializer,
                           LessonListSerializer,
                           QuickLessonSerializer,
                            )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from vocab.models import VocabBank
from lessons.models import (
                           Lesson,
                           LessonVocabBank,
                           SavedLesson,
                           Profile
                           )



class LessonFilter(django_filter.FilterSet):
    tags = django_filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Lesson
        fields = ('source_language', 'target_language', 'curator__username')


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

class LessonViewSet(viewsets.ModelViewSet):

   queryset = Lesson.objects.all().select_related('curator__user_profile').order_by("-curation_date")
   lookup_field = "slug"
   serializer_class = LessonSerializer
   permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

   def perform_create(self, serializer):
      serializer.save(curator=self.request.user)
      self.request.user.user_profile.points += 5
      # Grant another 10 for publishing (and 10 for each user who completes it)
      self.request.user.user_profile.save()
      return Response(serializer.data, status=status.HTTP_200_OK)


   def partial_update(self, request, slug):
      lesson = get_object_or_404(Lesson, slug=slug)
      serializer_context = {"request": request}
      serializer=LessonSerializer(lesson, data=request.data, partial=True)
      if serializer.is_valid():
         serializer.save()
      updatedserializer=LessonSerializer(lesson, context=serializer_context)
      return Response(updatedserializer.data)


   def list(self, request):
      queryset = Lesson.objects.filter(Q(published = True) |
                                    Q(curator = request.user)
                                    ).select_related(
                                       'curator__user_profile',
                                       'target_language',
                                       'source_language',
                                       'topic',
                                       'primary_vocab',
                                    ).prefetch_related(
                                       # 'savedlesson_set',
                                       'saves__curator',
                                       'upvote',
                                       'downvote',
                                       'flag',
                                       'hidden',
                                       'lessonvocabbank_set'
                                    ).order_by("-curation_date")

      profile = Profile.objects.prefetch_related('learninglanguage').get(user=request.user)
      serializer_context = {"request": request, "userlanguages": profile.learninglanguage.all(), "profile": profile}
      page = self.paginate_queryset(queryset)
      if page is not None:
         serializer = LessonSerializer(page, many=True, context=serializer_context) 
         return self.get_paginated_response(serializer.data)

      serializer = LessonSerializer(queryset, many=True, context=serializer_context) 
      return Response(serializer.data)


def quick_lesson_list(request):
   if request.user.is_authenticated:
      if request.method == 'GET':
         resdata = {}
         queryset = Lesson.objects.all().select_related('curator', 'curator__user_profile', 'source_language', 'target_language')
         return Response(QuickLessonSerializer(queryset, many=True).data)
      else:
         return Response(status=status.HTTP_401_UNAUTHORIZED)
   else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)


class QuickLessonList(generics.ListAPIView):
    model = Lesson
    serializer_class = LessonListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LessonFilter
    search_fields = ['title', 'description', 'object', 'lesson_type']
    ordering_fields = ['title',
                       'curation_date', 'updated', 'source_language']
    ordering = ['-curation_date']

    def get_queryset(self):
      #   user_upvote_queryset = LessonUpVote.objects.filter(user=self.request.user)
      #   user_downvote_queryset = LessonDownVote.objects.filter(user=self.request.user)
        queryset = Lesson.objects.filter(suspended=False).exclude(hides__user=self.request.user).select_related(
            'curator__user_profile', 'source_language', 'target_language'
        ).prefetch_related(
            'saves'
        ).annotate(
            user_has_saved=Exists(
                SavedLesson.objects.filter(
                    lesson=OuterRef('pk'), 
                    user=self.request.user
                ))
        )
      # .prefetch_related(
      #       Prefetch('upvotes', queryset=user_upvote_queryset, to_attr='user_upvote')
      #   ).prefetch_related(
      #       Prefetch('downvotes', queryset=user_downvote_queryset, to_attr='user_downvote')
      #   )
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}





class LessonVocabViewSet(viewsets.ModelViewSet):

   queryset = LessonVocabBank.objects.all().order_by("-curation_date")
   lookup_field = "pk"
   serializer_class = LessonVocabBankSerializer
   permission_classes = [IsAuthenticated, IsCuratorOrReadOnly]

   def perform_create(self, serializer):
      serializer.save(curator=self.request.user)
      self.request.user.user_profile.points += 3
      self.request.user.user_profile.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_lesson_vocab(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
         resdata = {}
         lesson = get_object_or_404(Lesson, pk=int(request.data.get('lesson_id')))
         if lesson.curator == request.user:
            if lesson.primary_vocab == None:
               bank = VocabBank.objects.create(curator=request.user)
               lesson.primary_vocab = bank
               lesson.save()
               resdata['vocab_bank_id'] = bank.pk
               return Response(resdata)
            else:
               resdata['vocab_bank_id'] = lesson.primary_vocab.pk
               return Response(resdata)
         else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
   else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def lesson_togglesaved(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            lesson = get_object_or_404(
                Lesson, pk=int(request.data['pk']))
            savings = SavedLesson.objects.filter(lesson=int(
                request.data['pk']), curator=request.user).first()
            if savings:
                print("Element Deleted")
                savings.delete()
                resdata['message'] = "Successfully removed item from saved list"
                resdata['success'] = True
            else:
                print("Element Saved")
                savings = SavedLesson.objects.create(
                    lesson=lesson, curator=request.user)
                resdata['message'] = "Successfully added item to saved list"
                resdata['success'] = True
        return Response(resdata)



@api_view(['POST'])
def lesson_togglehidden(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         lesson = get_object_or_404(Lesson, pk=int(request.data['pk']))
         if request.user in lesson.hidden.all():
            lesson.hidden.remove(request.user)
            lesson.save()
            resdata['message'] = "Successfully removed item from hidden list"
            resdata['success'] = True
         else: 
            lesson.hidden.add(request.user)
            lesson.save()
            resdata['message'] = "Successfully added item to hidden list"
            resdata['success'] = True
   return Response(resdata)

@api_view(['POST'])
def lesson_togglevote(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         lesson = get_object_or_404(Lesson, slug=request.data['slug'])
         if request.data['vote'] == "up":
            resdata['newuservote'] = 1
            if request.user in lesson.downvote.all():
               lesson.downvote.remove(request.user)
               lesson.save()
            if request.user not in lesson.upvote.all():
               lesson.upvote.add(request.user)
               lesson.save()
            resdata['message'] = "Successfully upvoted the lesson!"
            resdata['success'] = True

         elif request.data['vote'] == "down":
            resdata['newuservote'] = -1
            if request.user in lesson.upvote.all():
               lesson.upvote.remove(request.user)
               lesson.save()
            if request.user not in lesson.downvote.all():
               lesson.downvote.add(request.user)
               lesson.save()
            resdata['message'] = "Successfully downvoted the lesson!"
            resdata['success'] = True
         resdata['newupcount'] = lesson.upvote.all().count()
         resdata['newdowncount'] = lesson.downvote.all().count()
         
      return Response(resdata)

@api_view(['GET'])
def saved_lessons(request):
   if request.method == 'GET':
      resdata = {}
      if request.user.is_authenticated:
         lessons = Lesson.objects.filter(suspended=False, published=True).select_related(
            'curator__user_profile', 'source_language', 'target_language'
        ).prefetch_related(
                Prefetch('saves', queryset=SavedLesson.objects.filter(user=request.user))
            )
         serializer_context = {"request": request}
         serializer = LessonListSerializer(lessons, many=True, context=serializer_context)
         # resdata['count'] = lessons.count()
         return Response(serializer.data)

