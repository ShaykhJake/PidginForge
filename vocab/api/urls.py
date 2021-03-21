from django.urls import path, include, re_path
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
        LexemePairViewSet,
        CardStackList,
        CardStackViewSet,
        stack_togglesave,
        FavoriteStackViewSet,
        learn_stack_view,
        add_stack_pair,
        delete_stack_pair,
        get_lexeme_list,
        get_word_list,
        get_sentence_search,
        wordpair_list,
        get_lexemepair_list,
        add_pair_to_vocab_bank,
        remove_pair_from_bank,
        lexeme_definition_list,
        lexeme_pronunciation_list,
        lexeme_word_list,
        update_lexeme_learning_correct,
        update_lexeme_learning_incorrect,
    )   

app_name = 'vocab'

lexeme_router = DefaultRouter()
lexeme_router.register(r"lexemez", LexemeViewSet)

lexeme_definition_router = DefaultRouter()
lexeme_definition_router.register(r"lexemedefinitionz", LexemeDefinitionViewSet)

lexeme_pair_router = DefaultRouter()
lexeme_pair_router.register(r"lexemepairz", LexemePairViewSet)


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

card_stack_router = DefaultRouter()
card_stack_router.register(r"cardstackz", CardStackViewSet)

favorite_stack_router = DefaultRouter()
favorite_stack_router.register(r"favoritestackz", FavoriteStackViewSet, basename='FavoriteStack')


# learn_stack_router = DefaultRouter()
# learn_stack_router.register(r"learnstack", LearnStackViewSet)



urlpatterns = [
    path("", include(lexeme_router.urls)),
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
    path("", include(card_stack_router.urls)),
    path("", include(lexeme_pair_router.urls)),
    path("", include(favorite_stack_router.urls)),
    re_path('^stacks/list/$', CardStackList.as_view(), name="stack_list"),
    path('stacks/save/', stack_togglesave, name="stack_togglesave"),
    path('learnstack/<str:slug>/', learn_stack_view, name="learn_stack_view"),
    path('sentences/searchwords/<int:pk>/', get_sentence_search, name="get_sentences_search"),
    path('words/wordlist/', get_word_list, name="get_word_list"),
    path('words/pairings/<int:pk>/', wordpair_list, name="wordpair_list"),
    path('lexemes/lexemelist/', get_lexeme_list, name="get_lexeme_list"),
    path('lexemes/pairlist/<str:slug>/<str:pairlanguage>/', get_lexemepair_list, name="get_lexemepair_list"),
    path('lexemes/definitionlist/<str:slug>/', lexeme_definition_list, name="lexeme_definition_list"),
    path('lexemes/pronunciationlist/<str:slug>/', lexeme_pronunciation_list, name="lexeme_pronunciation_list"),
    path('lexemes/wordlist/<str:slug>/', lexeme_word_list, name="lexeme_word_list"),
    path('addpair/', add_pair_to_vocab_bank, name="add_pair_to_vocab_bank"),
    path('addstackpair/', add_stack_pair, name="add_stack_pair"),
    path('deletestackpair/', delete_stack_pair, name="delete_stack_pair"),
    path('removepair/', remove_pair_from_bank, name="remove_pair_from_bank"),
    path('lexemes/learning/correct/', update_lexeme_learning_correct, name="update_lexeme_learning_correct"),
    path('lexemes/learning/incorrect/', update_lexeme_learning_incorrect, name="update_lexeme_learning_incorrect"),
]
