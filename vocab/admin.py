from django.contrib import admin
from vocab.models import (
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
                        )


# Register your models here.

admin.site.register(WordRoot)
admin.site.register(Lexeme)
admin.site.register(LexemeGrammar)
admin.site.register(LexemeDefinition)
admin.site.register(LexemePronunciation)
admin.site.register(LexemeRoot)
admin.site.register(InflectedForm)
admin.site.register(InflectedFormGrammar)
admin.site.register(InflectedFormDefinition)
admin.site.register(InflectedFormPronunciation)
admin.site.register(InflectedFormImage)
admin.site.register(Sentence)
admin.site.register(InflectedFormSentence)
admin.site.register(SentenceTranslation)
admin.site.register(SentenceAudio)
admin.site.register(LexemePair)
admin.site.register(LexemePairLearning)
admin.site.register(InflectedFormPair)
admin.site.register(VocabBank)
admin.site.register(CardStack)