from django.urls import include, path
from rest_framework.routers import DefaultRouter
from questions.api import views as qv


router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("reply/post/", qv.post_reply, name="post-reply"),
    path("reply/edit/", qv.edit_reply, name="edit-reply"),
    path("reply/delete/<int:pk>/", qv.delete_reply, name="delete-reply"),
    path("questions/<slug:slug>/answers/", qv.AnswerListAPIView.as_view(), name="answer-list"),
    path("questions/<slug:slug>/answer/", qv.AnswerCreateAPIView.as_view(), name="answer-create"),
    path("answers/<int:pk>/", qv.AnswerRUDAPIView.as_view(), name="answer-detail"),
    path("answers/<int:pk>/like/", qv.AnswerLikeAPIView.as_view(), name="answer-like"),
    path('question/save/', qv.question_togglesave, name="question_togglesave"),
    path('question/vote/', qv.question_togglevote, name="question_togglevote"),
    path('question/hide/', qv.question_togglehide, name="question_togglehide"),
    path('answer/vote/', qv.answer_togglevote, name="answer_togglevote"),
    # path('list/', qv.get_question_list, name='question_list'),
    path('list/', qv.QuestionList.as_view(), name='question_list'),
    path('saved/', qv.saved_questions, name='saved_questions')
]