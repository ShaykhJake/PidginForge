from django.contrib import admin

# Register your models here.
from lessons.models import (
                     Lesson,
                     # LessonVocabBank
                     )


admin.site.register(Lesson)
# admin.site.register(LessonVocabBank)