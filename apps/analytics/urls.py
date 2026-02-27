"""
URL patterns for analytics app API.
"""

from django.urls import path
from .views import (
    AnalyticsReportListCreateView, AnalyticsReportDetailView,
    UserBehaviorTrackingListCreateView, LearningAnalyticsListView,
    LearningAnalyticsDetailView, DashboardWidgetListCreateView,
    DashboardWidgetDetailView, track_user_behavior,
    get_user_analytics_summary, get_platform_analytics
)

app_name = 'analytics'

urlpatterns = [
    path('reports/', AnalyticsReportListCreateView.as_view(), name='analytics_report_list'),
    path('reports/<uuid:pk>/', AnalyticsReportDetailView.as_view(), name='analytics_report_detail'),
    path('behavior/', UserBehaviorTrackingListCreateView.as_view(), name='user_behavior_list'),
    path('behavior/track/', track_user_behavior, name='track_user_behavior'),
    path('learning/', LearningAnalyticsListView.as_view(), name='learning_analytics_list'),
    path('learning/<uuid:pk>/', LearningAnalyticsDetailView.as_view(), name='learning_analytics_detail'),
    path('widgets/', DashboardWidgetListCreateView.as_view(), name='dashboard_widget_list'),
    path('widgets/<uuid:pk>/', DashboardWidgetDetailView.as_view(), name='dashboard_widget_detail'),
    path('summary/', get_user_analytics_summary, name='get_user_analytics_summary'),
    path('platform/', get_platform_analytics, name='get_platform_analytics'),
]
