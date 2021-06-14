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
                        LexemePairLearning,
                        InflectedFormPair,
                        VocabBank,
                        CardStack,
                        FavoriteStack,
                        )
from categories.models import Language
from categories.api.serializers import LanguageSerializer, MethodTagSerializer
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
    direction = serializers.SerializerMethodField()
    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only = False,
        slug_field='name',
    )

    class Meta:
        model = SentenceTranslation
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_direction(self, instance):
        return instance.language.direction

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
    inflectedforms = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()
    language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only = False,
        slug_field='name',
    )
    direction = serializers.SerializerMethodField()

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

    def get_inflectedforms(self, instance):
        inflectedforms = InflectedFormSentence.objects.filter(sentence = instance)
        words = []
        for i in inflectedforms:
            words.append(i.inflected_form)
        return SimpleInflectedFormSerializer(words, many=True).data

    def get_audio(self, instance):
        audio = SentenceAudio.objects.filter(sentence = instance)
        return SentenceAudioSerializer(audio, many=True).data

    def get_direction(self, instance):
        return instance.language.direction

class InflectedFormSentenceSerializer(serializers.ModelSerializer):
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    full_sentence = serializers.SerializerMethodField()
    
    class Meta:
        model = InflectedFormSentence
        fields = '__all__'
        # fields = ['id', 'curator', 'translations', 'curationdate', 'updated', 'user_vote', 'upvote_count', 'downvote_count', 'published']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_full_sentence(self, instance):
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
        fields = ['id', 'lemma', 'language', 'slug']


class SimpleInflectedFormSerializer(serializers.ModelSerializer):
    lexeme = SimpleLexemeSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    curator = CuratorSerializer(read_only=True)

    word = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = InflectedForm
        fields = ['id', 'language', 'word', 'lexeme', 'curator', 'curationdate']

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
    direction = serializers.SerializerMethodField(read_only=True)
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

    def get_direction(self, instance):
        return instance.language.direction

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
        # sentences = []
        # for inflected_sentence in inflected_sentences:
        #     sentences.append(inflected_sentence.sentence)
        return InflectedFormSentenceSerializer(inflected_sentences, many=True).data

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


   
class LexemePairSerializer(serializers.ModelSerializer):    
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    lexeme_1_details = serializers.SerializerMethodField(read_only=True)
    lexeme_2_details = serializers.SerializerMethodField(read_only=True)

    lexeme_1_language = serializers.SerializerMethodField(read_only=True)
    lexeme_2_language = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LexemePair
        fields = '__all__'
        # fields = ['id', 'curator', 'curationdate', 'side_a_text', 'side_a_hint', 'side_b_text', 'side_b_hint', 'side_a_language', 'a_direction', 'side_b_language', 'b_direction']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_lexeme_1_language(self, instance):
        serializer = LanguageSerializer(instance.lexeme_1.language)
        return serializer.data
    
    def get_lexeme_1_details(self, instance):
        serializer = SimpleLexemeSerializer(instance.lexeme_1)
        return serializer.data

    def get_lexeme_2_language(self, instance):
        serializer = LanguageSerializer(instance.lexeme_2.language)
        return serializer.data

    def get_lexeme_2_details(self, instance):
        serializer = SimpleLexemeSerializer(instance.lexeme_2)
        return serializer.data


class LexemePairLearningSerializer(serializers.ModelSerializer):
    curationdate = serializers.SerializerMethodField(read_only=True)
    last_attempted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LexemePairLearning
        fields = '__all__'
        # fields = ['id', 'curator', 'curationdate', 'side_a_text', 'side_a_hint', 'side_b_text', 'side_b_hint', 'side_a_language', 'a_direction', 'side_b_language', 'b_direction']
    
    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_last_attempted(self, instance):
        return instance.last_attempted.strftime("%B %d, %Y")

class LearnLexemePairSerializer(serializers.ModelSerializer):    
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    lexeme_1_details = serializers.SerializerMethodField(read_only=True)
    lexeme_2_details = serializers.SerializerMethodField(read_only=True)
    lexeme_1_language = serializers.SerializerMethodField(read_only=True)
    lexeme_2_language = serializers.SerializerMethodField(read_only=True)
    lexeme_1_audio = serializers.SerializerMethodField(read_only=True)
    lexeme_2_audio = serializers.SerializerMethodField(read_only=True)
    pair_learning = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LexemePair
        fields = '__all__'
        # fields = ['id', 'curator', 'curationdate', 'side_a_text', 'side_a_hint', 'side_b_text', 'side_b_hint', 'side_a_language', 'a_direction', 'side_b_language', 'b_direction']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_lexeme_1_language(self, instance):
        serializer = LanguageSerializer(instance.lexeme_1.language)
        return serializer.data
    
    def get_lexeme_1_details(self, instance):
        serializer = SimpleLexemeSerializer(instance.lexeme_1)
        return serializer.data

    def get_lexeme_2_language(self, instance):
        serializer = LanguageSerializer(instance.lexeme_2.language)
        return serializer.data

    def get_lexeme_2_details(self, instance):
        serializer = SimpleLexemeSerializer(instance.lexeme_2)
        return serializer.data

    def get_lexeme_1_audio(self, instance):
        # queryset = LexemePronunciation.objects.filter(lexeme=instance.lexeme_1)
        queryset = instance.lexeme_1.lexemepronunciation_set
        if queryset.exists():
            lexeme_audio = queryset.first()
            serializer = LexemePronunciationSerializer(lexeme_audio)
            return serializer.data
        # print(queryset)
        return False

    def get_lexeme_2_audio(self, instance):
        # queryset = LexemePronunciation.objects.filter(lexeme=instance.lexeme_2)
        queryset = instance.lexeme_2.lexemepronunciation_set
        if queryset.exists():
            lexeme_audio = queryset.first()
            serializer = LexemePronunciationSerializer(lexeme_audio)
            return serializer.data
        # print(queryset)
        return False

    def get_pair_learning(self, instance):
        user = self.context.get("request").user
        learnings = []
        queryset = instance.lexemepairlearning_set.filter(curator=user)
        if queryset.exists():
            learninglex = queryset[0]
        else:
            newpair = LexemePairLearning.objects.create(curator=user, lexeme_pair=instance)
            learninglex = newpair

        serializer = LexemePairLearningSerializer(learninglex)
        return serializer.data


class CardStackSerializer(serializers.ModelSerializer):    
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    l1direction = serializers.SerializerMethodField()
    l2direction = serializers.SerializerMethodField()

    learning_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )
    native_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )
    tags = serializers.ListField()
    lexeme_pairs = LexemePairSerializer(many=True, required=False)

    class Meta:
        model = CardStack
        fields = '__all__'
        read_only_fields = ('slug',)
        # fields = ['id', 'curator', 'curationdate', 'side_a_text', 'side_a_hint', 'side_b_text', 'side_b_hint', 'side_a_language', 'a_direction', 'side_b_language', 'b_direction']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_l1direction(self, instance):
        return instance.learning_language.direction

    def get_l2direction(self, instance):
        return instance.native_language.direction


class LearnStackSerializer(serializers.ModelSerializer):    
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    l1direction = serializers.SerializerMethodField()
    l2direction = serializers.SerializerMethodField()

    learning_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )
    native_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )
    tags = serializers.ListField(read_only=True)
    lexeme_pairs = LearnLexemePairSerializer(many=True, required=False)
    # lexeme_pairs = LearnLexemePairSerializer(many=True, required=False, context={'request': self.context.get('request')})
    # lexeme_pairs = LexemePairSerializer(many=True)
    # learning_pairs = serializers.SerializerMethodField()

    class Meta:
        model = CardStack
        fields = '__all__'
        read_only_fields = ('slug',)
        # fields = ['id', 'curator', 'curationdate', 'side_a_text', 'side_a_hint', 'side_b_text', 'side_b_hint', 'side_a_language', 'a_direction', 'side_b_language', 'b_direction']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_l1direction(self, instance):
        return instance.learning_language.direction

    def get_l2direction(self, instance):
        return instance.native_language.direction
    
    def get_learning_pairs(self, instance):
        user = self.context.get('request').user

        #TODO: Create a tuple or array for storing each learning pair, 
        # then, run through the algorithm below. Then, serialize this list
        # of new objects. THEN (and finally) return the list of lexeme pairs with all
        # of the user's information for those objects

        learnings = []
        # print("hello")
        # queryset = LexemePairLearning.objects.filter(curator=user)
        queryset = user.lexemepairlearning_set
        for i in instance.lexeme_pairs.all():
            # print(i)
            if queryset.filter(lexeme_pair=i).exists():
                learnings.append(queryset.filter(lexeme_pair=i)[0])
            else:
                newpair = LexemePairLearning.objects.create(curator=user, lexeme_pair=i)
                learnings.append(newpair)
        serializer = LexemePairLearningSerializer(learnings, many=True)
        return serializer.data
        

class LearningStackSerializer(serializers.ModelSerializer):    
    curator = CuratorSerializer(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    l1direction = serializers.SerializerMethodField()
    l2direction = serializers.SerializerMethodField()

    learning_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )
    native_language = serializers.SlugRelatedField(
        queryset = Language.objects.all(),
        read_only=False,
        slug_field='name',
    )
    tags = serializers.ListField(read_only=True)
    lexeme_pairs = LexemePairSerializer(many=True, required=False)

    class Meta:
        model = CardStack
        fields = '__all__'
        read_only_fields = ('slug',)
        # fields = ['id', 'curator', 'curationdate', 'side_a_text', 'side_a_hint', 'side_b_text', 'side_b_hint', 'side_a_language', 'a_direction', 'side_b_language', 'b_direction']

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")

    def get_l1direction(self, instance):
        return instance.learning_language.direction

    def get_l2direction(self, instance):
        return instance.native_language.direction


class QuickStackSerializer(serializers.Serializer):    
    curator = CuratorSerializer(read_only=True)
    name = serializers.CharField()
    slug = serializers.CharField()
    tags = serializers.ListField(read_only=True)
    curationdate = serializers.SerializerMethodField(read_only=True)
    learning_language = serializers.SerializerMethodField(read_only=True)
    native_language = serializers.SerializerMethodField(read_only=True)
    stats = serializers.SerializerMethodField(read_only=True)
    pair_count = serializers.SerializerMethodField(read_only=True)
    user_has_saved = serializers.BooleanField(read_only=True)

    # class Meta:
    #     model = CardStack
    #     fields = '__all__'

    def get_curationdate(self, instance):
        return instance.curationdate.strftime("%B %d, %Y")
    
    def get_updated(self, instance):
        return instance.updated.strftime("%B %d, %Y")
    
    def get_learning_language(self, instance):
        return instance.learning_language.name

    def get_native_language(self, instance):
        return instance.native_language.name 

    def get_pair_count(self, instance):
        return instance.lexeme_pairs.count()
    
    def get_stats(self, instance):
        user = self.context.get('request').user
        learning_pairs = LexemePairLearning.objects.filter(curator=user).filter(lexeme_pair__in=instance.lexeme_pairs.all())
        word_score = []
        for pair in learning_pairs:
            if pair.attempts > 0:
                word_score.append(pair.number_correct / pair.attempts)
        if len(word_score) > 0:
            mastery = int(sum(word_score)/len(word_score)*100)
        else:
            mastery = 0

        stats = {
            'cards_seen': len(learning_pairs),
            'mastery': mastery,
        }
        return stats

class FavoriteStackSerializer(serializers.ModelSerializer):
    stack_info = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteStack
        fields = '__all__'
        # fields = ['id', 'curator', 'curationdate', 'side_a_text', 'side_a_hint', 'side_b_text', 'side_b_hint', 'side_a_language', 'a_direction', 'side_b_language', 'b_direction']

    def get_stack_info(self, instance):
        request = self.context['request']
        serializer = QuickStackSerializer(instance.stack, context={'request':request})
        return serializer.data
