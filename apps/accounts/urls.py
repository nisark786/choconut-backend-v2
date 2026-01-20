from django.urls import path
from apps.accounts.views.signup_view import SignupView
from apps.accounts.views.login_view import LoginView
from apps.accounts.views.change_password_view import ChangePasswordView
from apps.accounts.views.me_view import MeView
from apps.accounts.views.refresh_token_view import CookieTokenRefreshView
from apps.accounts.views.logout_view import LogoutView
from apps.accounts.views.google_login_view import GoogleAuthView
from apps.accounts.views.otp_view import (
    StartOTPView,
    VerifyOTPView,
    ResendOTPView,
)


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path("google/", GoogleAuthView.as_view()),
    path("otp/start/", StartOTPView.as_view(),name='otp-start'),
    path("otp/verify/", VerifyOTPView.as_view(),name='otp-verify'),
    path("otp/resend/", ResendOTPView.as_view(),name='otp-resend'),
    path("login/", LoginView.as_view(),name='login'),
    path("me/", MeView.as_view(),name='me'),
    path("profile/change-password/", ChangePasswordView.as_view()),
    path("auth/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
