"""
URL patterns for personalization app API.
"""

from django.urls import path
from .views import (
    UserPreferenceDetailView, LearningPathListCreateView,
    LearningPathDetailView, RecommendationListView,
    RecommendationDetailView, UserActivityListCreateView,
    mark_recommendation_seen, mark_recommendation_acted_upon,
    track_user_activity, get_personalized_recommendations
)

app_name = 'personalization'

urlpatterns = [
    path('preferences/', UserPreferenceDetailView.as_view(), name='user_preference'),
    path('learning-paths/', LearningPathListCreateView.as_view(), name='learning_path_list'),
    path('learning-paths/<uuid:pk>/', LearningPathDetailView.as_view(), name='learning_path_detail'),
    path('recommendations/', RecommendationListView.as_view(), name='recommendation_list'),
    path('recommendations/<uuid:pk>/', RecommendationDetailView.as_view(), name='recommendation_detail'),
    path('recommendations/<uuid:pk>/seen/', mark_recommendation_seen, name='recommendation_seen'),
    path('recommendations/<uuid:pk>/acted/', mark_recommendation_acted_upon, name='recommendation_acted'),
    path('activities/', UserActivityListCreateView.as_view(), name='user_activity_list'),
    path('activities/track/', track_user_activity, name='track_user_activity'),
    path('get-recommendations/', get_personalized_recommendations, name='get_personalized_recommendations'),
]
