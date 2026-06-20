from django.urls import path


from .views import QuizView, QuizDetailView


urlpatterns = [
    path('quizzes/', QuizView.as_view(), name='quiz'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
]

