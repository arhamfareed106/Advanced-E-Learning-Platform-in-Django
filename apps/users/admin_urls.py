"""
URL patterns for admin dashboard.
"""

from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard_view, name='admin_dashboard'),
]
