from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from vocab.api.views import (
        LexemeViewSet,
        VocabBankViewSet,
        InflectedFormViewSet,
        InflectedFormPairViewSet,
        get_lexeme_list,
        get_word_list,
        wordpair_list,
        add_pair_to_vocab_bank,
        remove_pair_from_bank,
    )   

app_name = 'vocab'

lexeme_router = DefaultRouter()
lexeme_router.register(r"lexemez", LexemeViewSet)

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
    path("", include(inflected_form_pair_router.urls)),
    path('words/wordlist/', get_word_list, name="get_word_list"),
    path('words/pairings/<int:pk>/', wordpair_list, name="wordpair_list"),
    path('lexemes/lexemelist/', get_lexeme_list, name="get_lexeme_list"),
    path('addpair/', add_pair_to_vocab_bank, name="add_pair_to_vocab_bank"),
    path('removepair/', remove_pair_from_bank, name="remove_pair_from_bank"),
]
