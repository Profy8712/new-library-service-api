from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from .views import UserRegisterView, UserProfileView

urlpatterns = [
    path("users/", UserRegisterView.as_view(), name="user-register"),
    path("users/me/", UserProfileView.as_view(), name="user-profile"),
    path("users/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
