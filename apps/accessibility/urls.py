"""
URL patterns for accessibility app API.
"""

from django.urls import path
from .views import (
    AccessibilityPreferenceDetailView, WCAGComplianceListView,
    WCAGComplianceDetailView, AccessibilityFeedbackListCreateView,
    AccessibilityFeedbackDetailView, AccessibilityFeatureListView,
    submit_accessibility_feedback, get_user_accessibility_profile,
    get_wcag_compliance_summary
)

app_name = 'accessibility'

urlpatterns = [
    path('preferences/', AccessibilityPreferenceDetailView.as_view(), name='accessibility_preference'),
    path('wcag-compliance/', WCAGComplianceListView.as_view(), name='wcag_compliance_list'),
    path('wcag-compliance/<uuid:pk>/', WCAGComplianceDetailView.as_view(), name='wcag_compliance_detail'),
    path('feedback/', AccessibilityFeedbackListCreateView.as_view(), name='accessibility_feedback_list'),
    path('feedback/<uuid:pk>/', AccessibilityFeedbackDetailView.as_view(), name='accessibility_feedback_detail'),
    path('features/', AccessibilityFeatureListView.as_view(), name='accessibility_feature_list'),
    path('feedback/submit/', submit_accessibility_feedback, name='submit_accessibility_feedback'),
    path('profile/', get_user_accessibility_profile, name='get_user_accessibility_profile'),
    path('wcag-summary/', get_wcag_compliance_summary, name='get_wcag_compliance_summary'),
]
