from django.contrib import admin
from questions.models import Answer, Question, Reply
# Register your models here.


admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Reply)