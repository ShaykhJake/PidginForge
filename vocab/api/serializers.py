from rest_framework import serializers
from users.models import CustomUser, Profile
from vocab.models import  (
                        WordRoot, 
                        Lexeme,
                        LexemeGrammar,
                        LexemeDefinition,
                        LexemePronunciation,
                        LexemeRoot,
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
                        )
from categories.models import Language, TopicTag
from categories.api.serializers import LanguageSerializer, TopicTagSerializer, MethodTagSerializer
from django.db.models import Q

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'image']

class CuratorSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_profile']

class LexemeGrammarSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )

    class Meta:
        model = LexemeGrammar
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

class LexemeDefinitionSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    lexeme = serializers.SlugRelatedField(
        queryset = Lexeme.objects.all(),
        read_only=False,
        slug_field='slug',
    )

    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )

    direction = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LexemeDefinition
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_direction(self, instance):
        return instance.language.direction


class LexemePronunciationSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    lexeme = serializers.SlugRelatedField(
        queryset = Lexeme.objects.all(),
        read_only=False,
        slug_field='slug',
    )
    
    class Meta:
        model = LexemePronunciation
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

class InflectedFormGrammarSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    language = LanguageSerializer()

    class Meta:
        model = InflectedFormGrammar
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

class InflectedFormDefinitionSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )

    direction = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InflectedFormDefinition
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_direction(self, instance):
        return instance.language.direction


class InflectedFormPronunciationSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = InflectedFormPronunciation
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")



class InflectedFormImageSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = InflectedFormPronunciation
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")


class SentenceTranslationSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = SentenceTranslation
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

class SentenceAudioSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = SentenceAudio
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")



class SentenceSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    translations = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()
    language = LanguageSerializer()

    class Meta:
        model = Sentence
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_translations(self, instance):
        translations = SentenceTranslation.objects.filter(sentence = instance)
        return SentenceTranslationSerializer(translations, many=True).data
    
    def get_audio(self, instance):
        audio = SentenceAudio.objects.filter(sentence = instance)
        return SentenceAudioSerializer(audio, many=True).data

class InflectedFormSentenceSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    sentences = serializers.SerializerMethodField()
    

    class Meta:
        model = Sentence
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_sentences(self, instance):
        sentence = Sentence.objects.get(pk = instance.sentence.pk)
        return SentenceSerializer(sentence).data

class SimpleLexemeSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )

    class Meta:
        model = Lexeme
        fields = ['id', 'lemma', 'language']

class SimpleInflectedFormSerializer(serializers.ModelSerializer):
    lexeme = SimpleLexemeSerializer(read_only=True)
    language = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    word = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = InflectedForm
        fields = ['id', 'language', 'word', 'lexeme']

class InflectedFormPairSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    updated = serializers.SerializerMethodField(read_only=True)
    inflected_form_1 = SimpleInflectedFormSerializer()
    inflected_form_2 = SimpleInflectedFormSerializer()

    class Meta:
        model = InflectedFormPair
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")


class InflectedFormCreateSerializer(serializers.ModelSerializer):
    # curator = CuratorSerializer(read_only=True)
    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )

    class Meta:
        model = InflectedForm
        # fields = '__all__'
        fields = ['language', 'word', 'id']

  

class InflectedFormSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    updated = serializers.SerializerMethodField(read_only=True)
    
    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )
    word = serializers.CharField(max_length=255)
    curator_note = serializers.CharField(max_length=255)

    # Nested Information
    lexeme = SimpleLexemeSerializer(read_only=True)
    grammars = serializers.SerializerMethodField(read_only=True)
    definitions = serializers.SerializerMethodField(read_only=True)
    pronunciations = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    # word_pairs = serializers.SerializerMethodField(read_only=True)
    word_pair_count = serializers.SerializerMethodField(read_only=True)
    sentences = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InflectedForm
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_grammars(self, instance):
        grammars = InflectedFormGrammar.objects.filter(inflected_form = instance)
        return InflectedFormGrammarSerializer(grammars, many=True).data

    def get_definitions(self, instance):
        definitions = InflectedFormDefinition.objects.filter(inflected_form = instance)
        return InflectedFormDefinitionSerializer(definitions, many=True).data

    def get_pronunciations(self, instance):
        pronunciations = InflectedFormPronunciation.objects.filter(inflected_form = instance)
        return InflectedFormPronunciationSerializer(pronunciations, many=True).data

    def get_images(self, instance):
        images = InflectedFormImage.objects.filter(inflected_form = instance)
        return InflectedFormImageSerializer(images, many=True).data

    def get_sentences(self, instance):
        sentences = InflectedFormSentence.objects.filter(inflected_form = instance)
        return InflectedFormSentenceSerializer(sentences, many=True).data

    def get_sentences(self, instance):
        inflected_sentences = InflectedFormSentence.objects.filter(inflected_form = instance)
        sentences = []
        for inflected_sentence in inflected_sentences:
            sentences.append(inflected_sentence.sentence)
        return SentenceSerializer(sentences, many=True).data

    def get_word_pair_count(self, instance):
        pair1 = instance.inflected_form_pair_1.all()
        pair2 = instance.inflected_form_pair_2.all()
        return pair1.count() + pair2.count()






class LexemeSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    updated = serializers.SerializerMethodField(read_only=True)

    # Required Fields
    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
        )
    lemma = serializers.CharField(max_length=255)

    # Nested
    direction = serializers.SerializerMethodField(read_only=True)
    grammars = serializers.SerializerMethodField(read_only=True)
    definitions = serializers.SerializerMethodField(read_only=True)
    pronunciations = serializers.SerializerMethodField(read_only=True)
    inflected_forms = serializers.SerializerMethodField(read_only=True)

    # user_vote = serializers.SerializerMethodField()
    # upvote_count = serializers.SerializerMethodField()
    # downvote_count = serializers.SerializerMethodField()
    # forks_count = serializers.SerializerMethodField()


    class Meta:
        model = Lexeme
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_grammars(self, instance):
        grammars = LexemeGrammar.objects.filter(lexeme = instance)
        return LexemeGrammarSerializer(grammars, many=True).data

    def get_direction(self, instance):
        return instance.language.direction

    def get_definitions(self, instance):
        definitions = LexemeDefinition.objects.filter(lexeme = instance)
        return LexemeDefinitionSerializer(definitions, many=True).data

    def get_pronunciations(self, instance):
        pronunciations = LexemePronunciation.objects.filter(lexeme = instance)
        return LexemePronunciationSerializer(pronunciations, many=True).data

    def get_inflected_forms(self, instance):
        inflected_forms = InflectedForm.objects.filter(lexeme = instance)
        return InflectedFormSerializer(inflected_forms, many=True).data


    # def get_user_vote(self, instance):
    #     request = self.context.get("request")
    #     if instance.upvote.filter(pk=request.user.pk).exists():
    #         return 1
    #     elif instance.downvote.filter(pk=request.user.pk).exists():
    #         return -1
    #     else:
    #         return 0

    # def get_upvote_count(self, instance):
    #     return instance.upvote.count()

    # def get_downvote_count(self, instance):
    #     return instance.downvote.count()

    # def get_forks_count(self, instance):
    #     return instance.forks.count()


class VocabBankSerializer(serializers.ModelSerializer):    
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    word_pairs = InflectedFormPairSerializer(many=True)

    class Meta:
        model = VocabBank
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")
