from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, action

# from malapropos.api.serializers import (
#                            FlagSerializer,
#                             )

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from malapropos.models import Flag
from elements.models import YouTubeElement, AudioElement, TextElement
from questions.models import Question, Answer, Reply



class IsCuratorOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.curator == request.user


@api_view(['POST'])
def flag_item(request):
   if request.user.is_authenticated:
      resdata = {}
      if request.method == 'POST':
         contenttype = request.data['contenttype']
         pk = request.data['id']

         # Now we must determine what type of flag this is to associate the relationship
         if contenttype != None:
            if contenttype == 'Text':
               item = get_object_or_404(TextElement, pk=pk)
            elif contenttype == 'YouTube':
               item = get_object_or_404(YouTubeElement, pk=pk)
            elif contenttype == 'Audio':
               item = get_object_or_404(AudioElement, pk=pk)
            elif contenttype == 'question':
               item = get_object_or_404(Question, pk=pk)
            elif contenttype == 'answer':
               item = get_object_or_404(Answer, pk=pk)
            elif contenttype == 'answer_reply':
               item = get_object_or_404(Reply, pk=pk)
            elif contenttype == 'lesson':
               pass
            else:
               resdata['message'] = "There was something wrong with your request!"
               resdata['success'] = False
               return Response(resdata)

            if item.flag.filter(flagger=request.user).count() > 0:
               resdata['message'] = "Sorry, you can only flag once!"
               resdata['success'] = False
               return Response(resdata)

            else: 
               newflag = Flag()
               newflag.flagger = request.user
               newflag.reason = request.data['category']
               newflag.justification = request.data['justification']
               newflag.save()
               item.flag.add(newflag)
               item.save()

               strikes = item.flag.all().count()
               if strikes >= 3:
                  item.suspended = True
                  print(f"That is now {strikes} strikes. This item has been temporarily suspended where it will await further review!")
                  item.save()

               resdata['message'] = f"The new flag has been added! That's now {strikes} strikes!"
               resdata['success'] = True

         return Response(resdata)
   else:
      resdata['message'] = 'You must be signed in to flag items!'
      resdata['success'] = False

   return Response(resdata)


# for testing: { "category":"Copyright","justification":"really bad, dude", "contenttype":"youtube_element","id":"10","slug":"how-to-be-confident-in-any-situation-u6bf8c" }
