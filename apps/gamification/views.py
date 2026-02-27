"""
Views for gamification app.
"""

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum

from .models import Badge, UserBadge, Achievement, Leaderboard, PointsTransaction, LearningStreak
from .serializers import (
    BadgeSerializer, UserBadgeSerializer, AchievementSerializer,
    LeaderboardSerializer, PointsTransactionSerializer, LearningStreakSerializer
)
from apps.users.permissions import IsStudent


class BadgeListView(generics.ListAPIView):
    """List all available badges."""

    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [AllowAny]


class UserBadgeListView(generics.ListAPIView):
    """List badges earned by the current user."""

    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user).select_related('badge')


class AchievementListView(generics.ListAPIView):
    """List achievements for the current user."""

    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user).order_by('-created_at')


class LeaderboardView(generics.ListAPIView):
    """Get leaderboard rankings."""

    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Leaderboard.objects.all().order_by('-points', '-level')[:100]


class UserLeaderboardView(generics.RetrieveAPIView):
    """Get current user's leaderboard position."""

    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        leaderboard, created = Leaderboard.objects.get_or_create(user=self.request.user)
        return leaderboard


class PointsTransactionListView(generics.ListAPIView):
    """List points transactions for the current user."""

    serializer_class = PointsTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PointsTransaction.objects.filter(user=self.request.user).order_by('-created_at')


class LearningStreakView(generics.RetrieveAPIView):
    """Get current user's learning streak."""

    serializer_class = LearningStreakSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        streak, created = LearningStreak.objects.get_or_create(user=self.request.user)
        return streak


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def award_badge(request, badge_id):
    """Award a badge to the current user (admin/instructor only)."""
    if not (request.user.is_staff or request.user.is_instructor):
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    badge = get_object_or_404(Badge, id=badge_id)
    user_id = request.data.get('user_id')

    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    from apps.users.models import User
    user = get_object_or_404(User, id=user_id)

    user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)

    if not created:
        return Response({'message': 'Badge already awarded'}, status=status.HTTP_200_OK)

    return Response(UserBadgeSerializer(user_badge).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gamification_dashboard(request):
    """Get gamification dashboard for the current user."""
    user = request.user

    # Get user's badges
    user_badges = UserBadge.objects.filter(user=user).select_related('badge')

    # Get user's achievements
    achievements = Achievement.objects.filter(user=user).order_by('-created_at')[:10]

    # Get user's leaderboard position
    leaderboard, _ = Leaderboard.objects.get_or_create(user=user)

    # Get user's learning streak
    streak, _ = LearningStreak.objects.get_or_create(user=user)

    # Get points transactions
    total_points = PointsTransaction.objects.filter(user=user).aggregate(
        total=Sum('points')
    )['total'] or 0

    # Get recent transactions
    recent_transactions = PointsTransaction.objects.filter(user=user).order_by('-created_at')[:5]

    return Response({
        'badges': UserBadgeSerializer(user_badges, many=True).data,
        'achievements': AchievementSerializer(achievements, many=True).data,
        'leaderboard_position': leaderboard.rank,
        'points': total_points,
        'level': leaderboard.level,
        'streak': LearningStreakSerializer(streak).data,
        'recent_transactions': PointsTransactionSerializer(recent_transactions, many=True).data
    })
