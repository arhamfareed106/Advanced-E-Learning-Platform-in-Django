"""
URL patterns for course template views.
"""

from django.urls import path
from . import template_views

urlpatterns = [
    path('', template_views.course_list_view, name='course_list'),
    path('<slug:slug>/', template_views.course_detail_view, name='course_detail'),
]
