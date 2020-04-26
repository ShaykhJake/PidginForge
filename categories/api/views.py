from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from categories.api.permissions import IsAdminOrReadOnly
from categories.api.serializers import LanguageSerializer, TopicTagSerializer, MethodTagSerializer, GetLanguagesSerializer
from categories.models import Language, TopicTag, MethodTag
from rest_framework.decorators import api_view, action



class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all().order_by("name")
    lookup_field = "trigraph"
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class TopicTagViewSet(viewsets.ModelViewSet):
    queryset = TopicTag.objects.all().order_by("name")
    lookup_field = "name"
    serializer_class = TopicTagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class MethodTagViewSet(viewsets.ModelViewSet):
    queryset = MethodTag.objects.all().order_by("name")
    lookup_field = "name"
    serializer_class = MethodTagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


@api_view(['GET',])
def get_languages(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            languages = Language.objects.all().order_by("name")
            for language in languages:
                print(language.name)

            # languages = Language.objects.all().order_by("name")
            serializer = LanguageSerializer()
            return Response(serializer.data)

class ListLanguages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        languages = [language.name for language in Language.objects.all().order_by("name")]
        return Response(languages)

class ListTopics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        topics = [topic.name for topic in TopicTag.objects.all().order_by("name")]
        return Response(topics)