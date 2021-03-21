from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from django.db.models import Prefetch, Q, Exists, OuterRef, Count
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import AnswerSerializer, QuestionSerializer, QuestionListSerializer, ReplySerializer
import django_filters as django_filter
from .permissions import IsAuthorOrReadOnly
from questions.models import (
    Answer, 
    Question, 
    Reply, 
    QuestionUpVote, 
    QuestionDownVote, 
    QuestionSave,
    QuestionHide,
    AnswerUpVote, 
    AnswerDownVote
)

class QuestionFilter(django_filter.FilterSet):
    tags = django_filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Question
        fields = ('nativelanguage', 'learninglanguage', 'author__username', 'tags')


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    lookup_field = "slug"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        user_upvote_queryset = QuestionUpVote.objects.filter(user=self.request.user)
        user_downvote_queryset = QuestionDownVote.objects.filter(user=self.request.user)
        queryset = Question.objects.filter(suspended=False).select_related(
            'author__user_profile', 'nativelanguage', 'learninglanguage'
        ).prefetch_related(
            'saves', 'hides', 'upvotes', 'downvotes', 'answers', 'answers__author', 'answers__author__user_profile'
        ).annotate(
            user_has_saved=Exists(
                QuestionSave.objects.filter(
                    question=OuterRef('pk'), 
                    user=self.request.user
                ))
        ).prefetch_related(
            Prefetch('upvotes', queryset=user_upvote_queryset, to_attr='user_upvote')
        ).prefetch_related(
            Prefetch('downvotes', queryset=user_downvote_queryset, to_attr='user_downvote')
        )
        context = {
            "request": self.request
        }
        return queryset


    def retrieve(self, request, slug):
        user_upvote_queryset = QuestionUpVote.objects.filter(user=self.request.user)
        user_downvote_queryset = QuestionDownVote.objects.filter(user=self.request.user)
        queryset = Question.objects.filter(suspended=False).select_related(
            'author__user_profile', 'nativelanguage', 'learninglanguage'
        ).prefetch_related(
            'saves', 'hides', 'upvotes', 'downvotes', 'answers', 'answers__author', 'answers__author__user_profile'
        ).annotate(
            user_has_saved=Exists(
                QuestionSave.objects.filter(
                    question=OuterRef('pk'), 
                    user=self.request.user
                ))
        ).prefetch_related(
            Prefetch('upvotes', queryset=user_upvote_queryset, to_attr='user_upvote')
        ).prefetch_related(
            Prefetch('downvotes', queryset=user_downvote_queryset, to_attr='user_downvote')
        )
        question = get_object_or_404(queryset, slug=slug)
        context = {
            "request": self.request
        }
        serializer = QuestionSerializer(question, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        question = serializer.save(author=self.request.user)
        self.request.user.user_profile.points += 10
        self.request.user.user_profile.save()
        return Response(QuestionSerializer(question, context={"request":self.request}).data)

    def list(self, request):
        queryset = Question.objects.filter(
            suspended=False
            ).select_related(
                'author__user_profile', 'nativelanguage', 'learninglanguage'
            ).prefetch_related(
                'flag', 'saves', 'upvotes', 'downvotes', 'answers'
            ).order_by('-updated_at')
        context = { 'request': request }
        serializer = QuestionListSerializer(queryset, many=True, context=context)
        return Response(serializer.data)



class QuestionList(generics.ListAPIView):
    model = Question
    serializer_class = QuestionListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = QuestionFilter
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['title', 
                       'created_at', 'updated_at', 'learninglanguage']
    ordering = ['-created_at']

    def get_queryset(self):
        user=self.request.user
        user_upvote_queryset = QuestionUpVote.objects.filter(user=user)
        user_downvote_queryset = QuestionDownVote.objects.filter(user=user)
        queryset = Question.objects.filter(suspended=False).exclude(hides__user=user).select_related(
            'author__user_profile', 'nativelanguage', 'learninglanguage'
        ).prefetch_related(
            'saves', 'hides', 'upvotes', 'downvotes', 'answers'
        ).annotate(
            user_has_saved=Exists(
                QuestionSave.objects.filter(
                    question=OuterRef('pk'), 
                    user=user
                ))
        ).prefetch_related(
            Prefetch('upvotes', queryset=user_upvote_queryset, to_attr='user_upvote')
        ).prefetch_related(
            Prefetch('downvotes', queryset=user_downvote_queryset, to_attr='user_downvote')
        )
        by_preference = self.request.query_params.get('by_preference', None)
        by_saves = self.request.query_params.get('saved', None)
        if by_preference is not None:
            learning = user.user_profile.learninglanguage.all()
            native = user.user_profile.nativelanguage
            queryset = queryset.filter((Q(nativelanguage=native) & Q(learninglanguage__in=learning)) | 
                (Q(learninglanguage=native) & Q(nativelanguage__in=learning)))
        if by_saves is not None:
            queryset = queryset.filter(saves__user=user).order_by('-saves__created')
        return queryset
        return queryset


class QuestionList_OLD(generics.ListAPIView):
    
    queryset = Question.objects.filter(
        suspended=False
        ).select_related(
            'author__user_profile', 'nativelanguage', 'learninglanguage'
        ).prefetch_related(
            'flag', 'saved', 'upvote', 'downvote', 'answers'
        ).order_by('updated_at')
    # serializer_class = QuestionListSerializer

    def list(self, request):        
        queryset = Question.objects.filter(
            suspended=False
            ).select_related(
                'author__user_profile', 'nativelanguage', 'learninglanguage'
            ).prefetch_related(
                'flag', 'saved', 'upvote', 'downvote', 'answers'
            ).order_by('updated_at')
        # serializer_class = QuestionListSerializer
        # Note the use of `get_queryset()` instead of `self.queryset`
        # queryset = self.get_queryset()
        
        context = { "request": request, "bob": 'sexytime' }

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = QuestionListSerializer(page, many=True, context=context) 
            return self.get_paginated_response(serializer.data)

        serializer = QuestionListSerializer(queryset, many=True, context=context)
        return Response(serializer.data)


@api_view(['GET'])
def get_question_list(request):
    queryset = Question.objects.filter(
        suspended=False
        ).select_related(
            'author__user_profile', 'nativelanguage', 'learninglanguage'
        ).prefetch_related(
            'flag', 'saved', 'upvote', 'downvote', 'answers'
        ).order_by('-updated_at')

    serializer = QuestionListSerializer(queryset, many=True)

    return Response(serializer.data)


class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)
        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")
        user = self.request.user
        user.user_profile.points += 10
        user.user_profile.save()
        serializer.save(author=request_user, question=question)
        


class AnswerListAPIView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        answers = Answer.objects.filter(question__slug=kwarg_slug).order_by('-created_at')
        return answers

class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class AnswerLikeAPIView(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def saved_questions(request):
   if request.method == 'GET':
      resdata = {}
      if request.user.is_authenticated:
         questions = Question.objects.filter(suspended=False).select_related(
            'author__user_profile', 'nativelanguage', 'learninglanguage'
        ).prefetch_related('upvotes','downvotes').prefetch_related(
                Prefetch('saves', queryset=QuestionSave.objects.filter(user=request.user))
            )
         serializer_context = {"request": request}
         serializer = QuestionListSerializer(questions, many=True, context=serializer_context)
         # resdata['count'] = lessons.count()
         return Response(serializer.data)



# Toggle Hide Question

# Toggle Vote Question

# Toggle Hide Answer

# Toggle Vote Answer

# Post Reply
@api_view(['POST',])
def post_reply(request):
    resdata = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            answer = get_object_or_404(Answer, pk=int(request.data['answerpk']))
            reply = Reply()

            reply.answer = answer
            reply.author = request.user
            reply.content = request.data['content']
            reply.save()
            resdata['message'] = 'Successfully added the reply!'
            resdata['success'] = True
            resdata['id'] = reply.pk
            resdata['data'] = ReplySerializer(reply, context={'request': request}).data
        else:
            resdata['message'] = 'You must be logged in to reply to answers!'
            resdata['success'] = False
    else:
        resdata['message'] = 'Unknown Failure'
        resdata['success'] = False

    return Response(resdata)

# Edit Reply
@api_view(['PATCH',])
def edit_reply(request):
    resdata = {}
    if request.method == 'PATCH':
        if request.user.is_authenticated:
            reply = get_object_or_404(Reply, pk=int(request.data['pk']))
            if reply.author == request.user:
                reply.content = request.data['content']
                reply.save()
                resdata['message'] = 'Successfully edited the reply!'
                resdata['success'] = True
                resdata['newcontent'] = reply.content
            else:
                resdata['message'] = 'You must be the reply author to edit!'
                resdata['success'] = False
        else:
            resdata['message'] = 'You must be logged in to reply to answers!'
            resdata['success'] = False
    else:
        resdata['message'] = 'Unknown Failure'
        resdata['success'] = False
    return Response(resdata)


# Delete Reply
@api_view(['DELETE'])
def delete_reply(request, pk):
    resdata = {}
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            reply = get_object_or_404(Reply, pk=pk)
            if reply.author == request.user:
                reply.delete()
                resdata['message'] = 'Reply successfully deleted!'
                resdata['success'] = True
            else:
                resdata['message'] = 'You must be the reply author to delete!'
                resdata['success'] = False
        else:
            resdata['message'] = 'You must be logged in to delete replies!'
            resdata['success'] = False
    else:
        resdata['message'] = 'Unknown Failure'
        resdata['success'] = False
    return Response(resdata)




@api_view(['POST'])
def question_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                Question, pk=request.data['question_id'])

            if request.data['vote'] == "up":
                try:
                    downvote = QuestionDownVote.objects.get(user=request.user, question=element)
                except QuestionDownVote.DoesNotExist:
                    pass
                else:
                    downvote.delete()
                try:
                    upvote = QuestionUpVote.objects.get(user=request.user, question=element)
                except QuestionUpVote.DoesNotExist:
                    QuestionUpVote.objects.create(user=request.user, question=element)
                resdata['newuservote'] = 1
                resdata['message'] = "Successfully upvoted the question!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                try:
                    upvote = QuestionUpVote.objects.get(user=request.user, question=element)
                except QuestionUpVote.DoesNotExist:
                    pass
                else:
                    upvote.delete()
                try:
                    downvote = QuestionDownVote.objects.get(user=request.user, question=element)
                except QuestionDownVote.DoesNotExist:
                    downvote = QuestionDownVote.objects.create(user=request.user, question=element)
                resdata['newuservote'] = -1
                resdata['message'] = "Successfully downvoted the question!"
                resdata['success'] = True
            resdata['newupcount'] = element.upvotes.count()
            resdata['newdowncount'] = element.downvotes.count()

        return Response(resdata)

@api_view(['POST'])
def question_togglesave(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            try: 
                element = get_object_or_404(Question, slug=request.data['slug'])
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                saved = QuestionSave.objects.filter(user=request.user,question=element)
                if saved:
                    saved.delete()
                    resdata['message'] = "Successfully removed item from saved list"
                    resdata['success'] = True
                else:
                    QuestionSave.objects.create(user=request.user, question=element)
                    resdata['message'] = "Successfully added item to saved list"
                    resdata['success'] = True
    return Response(resdata)

@api_view(['POST'])
def question_togglehide(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            try: 
                element = get_object_or_404(Question, pk=request.data['pk'])
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                hidden = QuestionHide.objects.filter(user=request.user,question=element)
                if hidden:
                    hidden.delete()
                    resdata['message'] = "Successfully removed item from hidden list"
                    resdata['success'] = True
                    resdata['hidden'] = False
                else:
                    QuestionHide.objects.create(user=request.user, question=element)
                    resdata['message'] = "Successfully added item to hidden list"
                    resdata['success'] = True
                    resdata['hidden'] = True
    return Response(resdata)




@api_view(['POST'])
def answer_togglevote(request):
    if request.method == 'POST':
        resdata = {}
        if request.user.is_authenticated:
            element = get_object_or_404(
                Answer, pk=request.data['answer_id'])

            if request.data['vote'] == "up":
                try:
                    downvote = AnswerDownVote.objects.get(user=request.user, answer=element)
                except AnswerDownVote.DoesNotExist:
                    pass
                else:
                    downvote.delete()
                try:
                    upvote = AnswerUpVote.objects.get(user=request.user, answer=element)
                except AnswerUpVote.DoesNotExist:
                    AnswerUpVote.objects.create(user=request.user, answer=element)
                resdata['newuservote'] = 1
                resdata['message'] = "Successfully upvoted the answer!"
                resdata['success'] = True

            elif request.data['vote'] == "down":
                try:
                    upvote = AnswerUpVote.objects.get(user=request.user, answer=element)
                except AnswerUpVote.DoesNotExist:
                    pass
                else:
                    upvote.delete()
                try:
                    downvote = AnswerDownVote.objects.get(user=request.user, answer=element)
                except AnswerDownVote.DoesNotExist:
                    downvote = AnswerDownVote.objects.create(user=request.user, answer=element)
                resdata['newuservote'] = -1
                resdata['message'] = "Successfully downvoted the answer!"
                resdata['success'] = True
            resdata['newupcount'] = element.upvotes.count()
            resdata['newdowncount'] = element.downvotes.count()

        return Response(resdata)

# @api_view(['POST'])
# def question_togglesaved(request):
#    if request.method == 'POST':
#       resdata = {}
#       if request.user.is_authenticated:
#          question = get_object_or_404(Question, slug=request.data['slug'])
#          if request.user in question.saved.all():
#             question.saved.remove(request.user)
#             question.save()
#             resdata['message'] = "Successfully removed item from saved list"
#             resdata['success'] = True
#          else: 
#             question.saved.add(request.user)
#             question.save()
#             resdata['message'] = "Successfully added item to saved list"
#             resdata['success'] = True
#    return Response(resdata)

# @api_view(['POST'])
# def answer_togglevote(request):
#    if request.method == 'POST':
#       resdata = {}
#       if request.user.is_authenticated:
#          answer = get_object_or_404(Answer, pk=int(request.data['pk']))
#          if request.data['vote'] == "up":
#             resdata['newuservote'] = 1
#             if request.user in answer.downvote.all():
#                answer.downvote.remove(request.user)
#                answer.save()
#             if request.user not in answer.upvote.all():
#                answer.upvote.add(request.user)
#                answer.save()
#             resdata['message'] = "Successfully upvoted the answer!"
#             resdata['success'] = True

#          elif request.data['vote'] == "down":
#             resdata['newuservote'] = -1
#             if request.user in answer.upvote.all():
#                answer.upvote.remove(request.user)
#                answer.save()
#             if request.user not in answer.downvote.all():
#                answer.downvote.add(request.user)
#                answer.save()
#             resdata['message'] = "Successfully downvoted the answer!"
#             resdata['success'] = True
#          resdata['newupcount'] = answer.upvote.all().count()
#          resdata['newdowncount'] = answer.downvote.all().count()
         
#       return Response(resdata)

