from rest_framework import serializers
from categories.models import Language, TopicTag, MethodTag

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name','trigraph','direction']

class GetLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name']


class TopicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicTag
        fields = ['name']

class MethodTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodTag
        fields = ['name']

