"""
URL patterns for user authentication and profile.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, CustomTokenObtainPairView, EmailVerificationView,
    PasswordResetRequestView, PasswordResetConfirmView,
    UserProfileView, ProfileUpdateView, UserListView,
    SocialLoginView, MagicLinkRequestView, MagicLinkLoginView,
    OTPRequestView, OTPVerifyView, TwoFactorSetupView,
    TwoFactorVerifyView, TwoFactorDisableView, TwoFactorLoginView,
    TwoFactorLoginVerifyView
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TwoFactorLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email'),
    
    # Password reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Profile
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    
    # User list (admin)
    path('users/', UserListView.as_view(), name='user_list'),
    
    # Social authentication
    path('social-login/', SocialLoginView.as_view(), name='social_login'),
    
    # Passwordless authentication
    path('magic-link-request/', MagicLinkRequestView.as_view(), name='magic_link_request'),
    path('magic-link-login/', MagicLinkLoginView.as_view(), name='magic_link_login'),
    path('otp-request/', OTPRequestView.as_view(), name='otp_request'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp_verify'),
    
    # 2FA authentication
    path('2fa/setup/', TwoFactorSetupView.as_view(), name='two_factor_setup'),
    path('2fa/verify/', TwoFactorVerifyView.as_view(), name='two_factor_verify'),
    path('2fa/disable/', TwoFactorDisableView.as_view(), name='two_factor_disable'),
    path('2fa/login/', TwoFactorLoginView.as_view(), name='two_factor_login'),
    path('2fa/login-verify/', TwoFactorLoginVerifyView.as_view(), name='two_factor_login_verify'),
]
