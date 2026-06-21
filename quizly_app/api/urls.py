from django.urls import path


from .views import QuizView, QuizDetailView


"""
URL configuration for the Quizly API endpoints.
These routes expose quiz list/create functionality and
quiz detail/update/delete functionality.
"""


urlpatterns = [
    path('quizzes/', QuizView.as_view(), name='quiz'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
]
