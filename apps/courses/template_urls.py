"""
URL patterns for course template views.
"""

from django.urls import path
from . import template_views

urlpatterns = [
    path('', template_views.course_catalog_view, name='course_catalog'),
    path('<slug:slug>/', template_views.course_detail_view, name='course_detail'),
    path('<slug:slug>/enroll/', template_views.enroll_course, name='enroll_course'),
    path('<slug:slug>/lessons/<int:lesson_id>/', template_views.lesson_detail_view, name='lesson_detail'),
    path('<slug:slug>/lessons/<int:lesson_id>/complete/', template_views.mark_lesson_complete, name='mark_lesson_complete'),
]
