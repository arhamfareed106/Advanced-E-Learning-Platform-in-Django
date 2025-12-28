from django.urls import path
from . import views

urlpatterns = [
    # Accessibility Preferences URLs
    path('preferences/', views.AccessibilityPreferenceDetailView.as_view(), name='accessibility-preferences'),
    
    # WCAG Compliance URLs
    path('wcag-compliance/', views.WCAGComplianceListView.as_view(), name='wcag-compliance-list'),
    path('wcag-compliance/<uuid:pk>/', views.WCAGComplianceDetailView.as_view(), name='wcag-compliance-detail'),
    path('wcag-compliance/summary/', views.get_wcag_compliance_summary, name='wcag-compliance-summary'),
    
    # Accessibility Feedback URLs
    path('feedback/', views.AccessibilityFeedbackListCreateView.as_view(), name='accessibility-feedback-list-create'),
    path('feedback/<uuid:pk>/', views.AccessibilityFeedbackDetailView.as_view(), name='accessibility-feedback-detail'),
    path('feedback/submit/', views.submit_accessibility_feedback, name='submit-accessibility-feedback'),
    
    # Accessibility Features URLs
    path('features/', views.AccessibilityFeatureListView.as_view(), name='accessibility-features'),
    
    # User Accessibility Profile
    path('profile/', views.get_user_accessibility_profile, name='user-accessibility-profile'),
]