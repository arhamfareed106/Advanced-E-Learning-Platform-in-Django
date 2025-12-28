from django.urls import path
from . import views

urlpatterns = [
    # Analytics Reports URLs
    path('reports/', views.AnalyticsReportListCreateView.as_view(), name='analytics-report-list-create'),
    path('reports/<uuid:pk>/', views.AnalyticsReportDetailView.as_view(), name='analytics-report-detail'),
    
    # User Behavior Tracking URLs
    path('behavior/', views.UserBehaviorTrackingListCreateView.as_view(), name='user-behavior-list-create'),
    path('behavior/track/', views.track_user_behavior, name='track-user-behavior'),
    
    # Learning Analytics URLs
    path('learning/', views.LearningAnalyticsListView.as_view(), name='learning-analytics-list'),
    path('learning/<uuid:pk>/', views.LearningAnalyticsDetailView.as_view(), name='learning-analytics-detail'),
    
    # Dashboard Widgets URLs
    path('widgets/', views.DashboardWidgetListCreateView.as_view(), name='dashboard-widget-list-create'),
    path('widgets/<uuid:pk>/', views.DashboardWidgetDetailView.as_view(), name='dashboard-widget-detail'),
    
    # Analytics Summary URLs
    path('summary/', views.get_user_analytics_summary, name='user-analytics-summary'),
    path('platform/', views.get_platform_analytics, name='platform-analytics'),
]