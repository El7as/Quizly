from django.contrib import admin


from .models import Question, Quiz, Option


"""
Register the Quiz-related models in the Django admin interface.
This allows administrators to view, edit, and manage quizzes,
questions, and answer options directly from the admin dashboard.
"""


admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Option)
