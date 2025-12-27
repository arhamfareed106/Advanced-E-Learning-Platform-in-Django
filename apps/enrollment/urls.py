"""
URL patterns for enrollment API.
"""

from django.urls import path
from .views import (
    EnrollmentListView, EnrollmentCreateView,
    LessonProgressUpdateView, EnrollmentDetailView
)

app_name = 'enrollment'

urlpatterns = [
    path('', EnrollmentListView.as_view(), name='enrollment_list'),
    path('enroll/', EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('<uuid:pk>/', EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('lesson/<uuid:lesson_id>/progress/', LessonProgressUpdateView.as_view(), name='lesson_progress'),
]
