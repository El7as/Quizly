from django.urls import path


from .views import RegisterView, LoginView, LogoutView, RefreshTokenView

"""
URL configuration for the authentication endpoints.
Each path maps an HTTP route to a corresponding class-based view.
"""

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),   
    path('token/refresh/', RefreshTokenView.as_view(), name='token/refresh/'),
]
