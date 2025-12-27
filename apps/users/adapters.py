"""
Custom adapters for django-allauth.
"""
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from allauth.account.utils import user_email, user_field


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter to handle user creation from social accounts.
    """
    
    def populate_user(self, request, user, data):
        """
        Populate user with data from social account.
        """
        user = super().populate_user(request, user, data)
        
        # Set email from social account data
        email = data.get('email')
        if email:
            user_email(user, email)
        
        # Set first and last name
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
            
        # Set username based on email if not provided
        if not user.username:
            username = data.get('username', email.split('@')[0])
            user.username = username
            
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter to handle social login/registration.
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider
        but before the login is actually processed.
        """
        super().pre_social_login(request, sociallogin)
        
        # Check if this is a new social login
        if not sociallogin.is_existing:
            # Get user data from social account
            user_data = sociallogin.account.extra_data
            
            # Get the user instance being created
            user = sociallogin.user
            
            # Set email verification status based on social provider
            email_verified = user_data.get('email_verified', True)  # Most providers verify emails
            user.is_email_verified = email_verified