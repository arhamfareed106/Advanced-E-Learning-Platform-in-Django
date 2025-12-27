"""
URL patterns for student enrollment template views.
"""

from django.urls import path
from . import template_views

urlpatterns = [
    path('dashboard/', template_views.student_dashboard_view, name='student_dashboard'),
]
