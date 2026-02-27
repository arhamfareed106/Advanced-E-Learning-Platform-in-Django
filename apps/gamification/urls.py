"""
URL patterns for gamification API.
"""

from django.urls import path
from .views import (
    BadgeListView, UserBadgeListView, AchievementListView,
    LeaderboardView, UserLeaderboardView, PointsTransactionListView,
    LearningStreakView, award_badge, gamification_dashboard
)

app_name = 'gamification'

urlpatterns = [
    path('badges/', BadgeListView.as_view(), name='badge_list'),
    path('my-badges/', UserBadgeListView.as_view(), name='user_badge_list'),
    path('achievements/', AchievementListView.as_view(), name='achievement_list'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('my-leaderboard/', UserLeaderboardView.as_view(), name='user_leaderboard'),
    path('transactions/', PointsTransactionListView.as_view(), name='points_transaction_list'),
    path('streak/', LearningStreakView.as_view(), name='learning_streak'),
    path('award-badge/<uuid:badge_id>/', award_badge, name='award_badge'),
    path('dashboard/', gamification_dashboard, name='gamification_dashboard'),
]
