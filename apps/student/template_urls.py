"""
URL patterns for student template views.
"""

from django.urls import path
from . import template_views

urlpatterns = [
    path('dashboard/', template_views.dashboard_view, name='student_dashboard'),
    path('my-courses/', template_views.my_courses_view, name='student_my_courses'),
    path('certificates/', template_views.certificates_view, name='student_certificates'),
    path('achievements/', template_views.achievements_view, name='student_achievements'),
]
