from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """
    Django application configuration for the authentication app.

    This class registers the app with Django and allows you to define
    application-specific settings, signals, or initialization logic.
    """
    
    name = 'auth_app'
