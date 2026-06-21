from django.contrib.auth.models import AbstractUser
from django.db import models



class  User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Adds:
        - A unique email field (required for authentication and registration).

    This model can be extended later with additional profile fields
    such as avatar, preferences, or statistics.
    """
        
    email = models.EmailField(unique=True)


    def __str__(self):
        """
        Return a readable string representation of the user.
        Useful for admin display and debugging.
        """

        return self.username
    