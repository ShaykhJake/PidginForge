from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from questions.api.serializers import AnswerSerializer, QuestionSerializer, ReplySerializer
from questions.api.permissions import IsAuthorOrReadOnly
from questions.models import Answer, Question, Reply

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    lookup_field = "slug"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("hello")
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug=kwarg_slug)

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this Question!")
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
            print(reply)

            print(answer.replies.all())

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
    print(resdata)
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
                print(reply)
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
                print(reply)
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
def question_togglesaved(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         question = get_object_or_404(Question, slug=request.data['slug'])
         if request.user in question.saved.all():
            question.saved.remove(request.user)
            question.save()
            resdata['message'] = "Successfully removed item from saved list"
            resdata['success'] = True
         else: 
            question.saved.add(request.user)
            question.save()
            resdata['message'] = "Successfully added item to saved list"
            resdata['success'] = True
   return Response(resdata)

@api_view(['POST'])
def answer_togglevote(request):
   if request.method == 'POST':
      resdata = {}
      if request.user.is_authenticated:
         answer = get_object_or_404(Answer, pk=int(request.data['pk']))
         if request.data['vote'] == "up":
            resdata['newuservote'] = 1
            if request.user in answer.downvote.all():
               answer.downvote.remove(request.user)
               answer.save()
            if request.user not in answer.upvote.all():
               answer.upvote.add(request.user)
               answer.save()
            resdata['message'] = "Successfully upvoted the answer!"
            resdata['success'] = True

         elif request.data['vote'] == "down":
            resdata['newuservote'] = -1
            if request.user in answer.upvote.all():
               answer.upvote.remove(request.user)
               answer.save()
            if request.user not in answer.downvote.all():
               answer.downvote.add(request.user)
               answer.save()
            resdata['message'] = "Successfully downvoted the answer!"
            resdata['success'] = True
         resdata['newupcount'] = answer.upvote.all().count()
         resdata['newdowncount'] = answer.downvote.all().count()
         
      return Response(resdata)

