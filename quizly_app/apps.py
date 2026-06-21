from django.apps import AppConfig


class QuizlyAppConfig(AppConfig):
    """
    Django application configuration for the Quizly app.

    This class registers the app with Django and can be extended later
    to include application-specific initialization logic or signals.
    """
        
    name = 'quizly_app'
