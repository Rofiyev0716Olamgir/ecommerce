# Two-Step Verification
# add-eplikeyshon_password
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    UserRegisterView,
    SendEmailView,
    VerifyEmailView,
    LoginView,
    ChangePasswordView,
    ResetPasswordView,
    UserProfileRUDView,
)

router = DefaultRouter()


class USerProfileRUDView:
    pass


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('mail/send/', SendEmailView.as_view(), name='send-mail'),
    path('mail/verify/', VerifyEmailView.as_view(), name='verify-mail'),
    path('login/', LoginView.as_view(), name='login'),
    path('pasword/change/', ChangePasswordView.as_view(), name='password-change'),
    path('pasword/reset/', ResetPasswordView.as_view(), name='password-reset'),
    path('profile/<int:pk>/', UserProfileRUDView.as_view(), name='profile'),
]
