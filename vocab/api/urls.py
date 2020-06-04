from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from vocab.api.views import (
        LexemeViewSet,
        VocabBankViewSet,
        InflectedFormViewSet,
        InflectedFormPairViewSet,
        SentenceViewSet,
        SentenceAudioViewSet,
        SentenceTranslationViewSet,
        InflectedSentenceViewSet,
        LexemeDefinitionViewSet,
        LexemePronunciationViewSet,
        InflectedFormDefinitionViewSet,
        InflectedFormPronunciationViewSet,
        get_lexeme_list,
        get_word_list,
        get_sentence_search,
        wordpair_list,
        add_pair_to_vocab_bank,
        remove_pair_from_bank,
        lexeme_definition_list,
        lexeme_pronunciation_list,
        lexeme_word_list,
    )   

app_name = 'vocab'

lexeme_router = DefaultRouter()
lexeme_router.register(r"lexemez", LexemeViewSet)

lexeme_definition_router = DefaultRouter()
lexeme_definition_router.register(r"lexemedefinitionz", LexemeDefinitionViewSet)

inflected_definition_router = DefaultRouter()
inflected_definition_router.register(r"inflecteddefinitionz", InflectedFormDefinitionViewSet)

lexeme_pronunciation_router = DefaultRouter()
lexeme_pronunciation_router.register(r"lexemepronunciationz", LexemePronunciationViewSet)

sentence_router = DefaultRouter()
sentence_router.register(r"sentencez", SentenceViewSet)

sentence_audio_router = DefaultRouter()
sentence_audio_router.register(r"sentenceaudioz", SentenceAudioViewSet)

sentence_translation_router = DefaultRouter()
sentence_translation_router.register(r"sentencetranslationz", SentenceTranslationViewSet)


inflected_sentence_router = DefaultRouter()
inflected_sentence_router.register(r"inflectedsentencez", InflectedSentenceViewSet)

inflected_pronunciation_router = DefaultRouter()
inflected_pronunciation_router.register(r"inflectedpronunciationz", InflectedFormPronunciationViewSet)


inflected_form_router = DefaultRouter()
inflected_form_router.register(r"inflectedformz", InflectedFormViewSet)

inflected_form_pair_router = DefaultRouter()
inflected_form_pair_router.register(r"inflectedpairz", InflectedFormPairViewSet)


vocab_bank_router = DefaultRouter()
vocab_bank_router.register(r"bank", VocabBankViewSet)


urlpatterns = [
    path("", include(lexeme_router.urls)),
    # path('youtube/save/', youtube_togglesaved, name="youtube_togglesaved"),
    # path('youtube/hide/', youtube_togglehidden, name="youtube_togglehidden"),
    # path('youtube/check/', youtube_check, name="youtube_check"),
    # path('youtube/vote/', youtube_togglevote, name="youtube_togglevote"),
    path("", include(inflected_form_router.urls)),
    path("", include(vocab_bank_router.urls)),
    path("", include(sentence_router.urls)),
    path("", include(sentence_audio_router.urls)),
    path("", include(sentence_translation_router.urls)),
    path("", include(inflected_sentence_router.urls)),
    path("", include(inflected_form_pair_router.urls)),
    path("", include(lexeme_definition_router.urls)),
    path("", include(lexeme_pronunciation_router.urls)),
    path("", include(inflected_definition_router.urls)),
    path("", include(inflected_pronunciation_router.urls)),
    path('sentences/searchwords/<int:pk>/', get_sentence_search, name="get_sentences_search"),
    path('words/wordlist/', get_word_list, name="get_word_list"),
    path('words/pairings/<int:pk>/', wordpair_list, name="wordpair_list"),
    path('lexemes/lexemelist/', get_lexeme_list, name="get_lexeme_list"),
    path('lexemes/definitionlist/<str:slug>/', lexeme_definition_list, name="lexeme_definition_list"),
    path('lexemes/pronunciationlist/<str:slug>/', lexeme_pronunciation_list, name="lexeme_pronunciation_list"),
    path('lexemes/wordlist/<str:slug>/', lexeme_word_list, name="lexeme_word_list"),
    path('addpair/', add_pair_to_vocab_bank, name="add_pair_to_vocab_bank"),
    path('removepair/', remove_pair_from_bank, name="remove_pair_from_bank"),
    
]
