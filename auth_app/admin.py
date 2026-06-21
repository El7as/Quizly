from django.contrib import admin


from .models import User


"""
Register the custom User model in the Django admin interface.
This allows administrators to view, edit, and manage user accounts
directly from the Django admin dashboard.
"""


admin.site.register(User)
