from django.urls import path
from . import views

urlpatterns = [
    # User Preferences URLs
    path('preferences/', views.UserPreferenceDetailView.as_view(), name='user-preferences'),
    
    # Learning Path URLs
    path('learning-paths/', views.LearningPathListCreateView.as_view(), name='learning-path-list-create'),
    path('learning-paths/<uuid:pk>/', views.LearningPathDetailView.as_view(), name='learning-path-detail'),
    
    # Recommendation URLs
    path('recommendations/', views.RecommendationListView.as_view(), name='recommendation-list'),
    path('recommendations/<uuid:pk>/', views.RecommendationDetailView.as_view(), name='recommendation-detail'),
    path('recommendations/<uuid:recommendation_id>/mark-seen/', views.mark_recommendation_seen, name='mark-recommendation-seen'),
    path('recommendations/<uuid:recommendation_id>/mark-acted-upon/', views.mark_recommendation_acted_upon, name='mark-recommendation-acted-upon'),
    path('recommendations/personalized/', views.get_personalized_recommendations, name='personalized-recommendations'),
    
    # User Activity URLs
    path('activities/', views.UserActivityListCreateView.as_view(), name='user-activity-list-create'),
    path('activities/track/', views.track_user_activity, name='track-user-activity'),
]