"""
Custom authentication backend for email-based authentication.
"""

from django.contrib.auth.backends import ModelBackend
from apps.users.models import User


class EmailBackend(ModelBackend):
    """
    Authenticate using email address instead of username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Allow authentication with email in the username field
        email = kwargs.get('email', username)
        
        if email is None or password is None:
            return None
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
