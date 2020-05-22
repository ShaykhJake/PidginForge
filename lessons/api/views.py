from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, action
from django.db.models import Q
from lessons.api.serializers import (
                           LessonSerializer,
                           LessonVocabBankSerializer,
                            )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from vocab.models import VocabBank
from lessons.models import (
                           Lesson,
                           LessonVocabBank,
                           )

# ISINVITED CLASS?
# class IsCuratorOrReadOnly(permissions.BasePermission):
    
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.curator == request.user


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

   queryset = Lesson.objects.all().order_by("-curationdate")
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
                                    ).order_by("-curationdate")

      userlanguages = request.user.user_profile.learninglanguage.all()
      usertopics = request.user.user_profile.learningtopics.all()


      serializer_context = {"request": request, "userlanguages": userlanguages, "usertopics": usertopics}
      
      # page = self.paginate_queryset(queryset)
      # if page is not None:
      #    serializer = LessonSerializer(page, many=True, context=serializer_context) 
      #    return self.get_paginated_response(serializer.data)

      page = self.paginate_queryset(queryset)
      if page is not None:
         serializer = LessonSerializer(page, many=True, context=serializer_context) 
         return self.get_paginated_response(serializer.data)

      serializer = LessonSerializer(queryset, many=True, context=serializer_context) 
      return Response(serializer.data)


class LessonVocabViewSet(viewsets.ModelViewSet):

   queryset = LessonVocabBank.objects.all().order_by("-curationdate")
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
      print('hello')
      if request.user.is_authenticated:
         print('hello')
         lesson = get_object_or_404(Lesson, pk=int(request.data['pk']))
         if request.user in lesson.saved.all():
            print('hello')
            lesson.saved.remove(request.user)
            lesson.save()
            resdata['message'] = "Successfully removed item from saved list"
            resdata['success'] = True
         else: 
            lesson.saved.add(request.user)
            lesson.save()
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

