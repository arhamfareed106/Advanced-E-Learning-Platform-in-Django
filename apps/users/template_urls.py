"""
URL patterns for user authentication and profile template views.
"""

from django.urls import path
from . import template_views

urlpatterns = [
    path('login/', template_views.login_view, name='login'),
    path('signup/', template_views.signup_view, name='signup'),
    path('logout/', template_views.logout_view, name='logout'),
    path('profile/', template_views.profile_view, name='profile'),
    path('profile/edit/', template_views.profile_edit_view, name='profile_edit'),
]
