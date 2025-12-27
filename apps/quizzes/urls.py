"""
URL patterns for quizzes API.
"""

from django.urls import path
from .views import (
    QuizListView, QuizDetailView, AttemptSubmitView,
    AttemptListView, AttemptDetailView
)

app_name = 'quizzes'

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('<uuid:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('attempts/', AttemptListView.as_view(), name='attempt_list'),
    path('attempts/<uuid:pk>/', AttemptDetailView.as_view(), name='attempt_detail'),
    path('submit/', AttemptSubmitView.as_view(), name='attempt_submit'),
]
