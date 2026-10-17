from django.urls import path
from .views import (
    SignupView,
    SigninView,
    SignoutView,
    CurrentUserView,
    ProfileUpdateView,
    ForgotPasswordView,
    PublicProfileView,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('profiles/<str:identifier>/', PublicProfileView.as_view(), name='public-profile'),
]

