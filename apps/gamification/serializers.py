"""
Serializers for gamification app.
"""

from rest_framework import serializers
from .models import Badge, UserBadge, Achievement, Leaderboard, PointsTransaction, LearningStreak
from apps.users.serializers import UserSerializer


class BadgeSerializer(serializers.ModelSerializer):
    """Serializer for badges."""

    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description', 'icon', 'color',
            'points_required', 'courses_required', 'lessons_completed',
            'quizzes_passed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserBadgeSerializer(serializers.ModelSerializer):
    """Serializer for user badges."""

    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'earned_at']
        read_only_fields = ['id', 'earned_at']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for achievements."""

    course = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = [
            'id', 'user', 'title', 'description', 'icon', 'points',
            'achievement_type', 'course', 'quiz', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_course(self, obj):
        if obj.course:
            return {
                'id': str(obj.course.id),
                'title': obj.course.title
            }
        return None

    def get_quiz(self, obj):
        if obj.quiz:
            return {
                'id': str(obj.quiz.id),
                'title': obj.quiz.title
            }
        return None


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for leaderboard."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'points', 'level', 'rank', 'last_updated']
        read_only_fields = ['id', 'last_updated']


class PointsTransactionSerializer(serializers.ModelSerializer):
    """Serializer for points transactions."""

    course = serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = PointsTransaction
        fields = [
            'id', 'user', 'transaction_type', 'points', 'description',
            'course', 'lesson', 'quiz', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_course(self, obj):
        if obj.course:
            return {'id': str(obj.course.id), 'title': obj.course.title}
        return None

    def get_lesson(self, obj):
        if obj.lesson:
            return {'id': str(obj.lesson.id), 'title': obj.lesson.title}
        return None

    def get_quiz(self, obj):
        if obj.quiz:
            return {'id': str(obj.quiz.id), 'title': obj.quiz.title}
        return None


class LearningStreakSerializer(serializers.ModelSerializer):
    """Serializer for learning streaks."""

    class Meta:
        model = LearningStreak
        fields = [
            'id', 'user', 'current_streak', 'longest_streak',
            'last_activity_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
