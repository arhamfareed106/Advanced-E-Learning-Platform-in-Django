"""
Serializers for personalization app.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserPreference, LearningPath, Recommendation, UserActivity

User = get_user_model()


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for user preferences."""

    class Meta:
        model = UserPreference
        fields = [
            'id', 'user', 'learning_style', 'difficulty_level',
            'preferred_language', 'study_time_preference',
            'notification_frequency', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class LearningPathSerializer(serializers.ModelSerializer):
    """Serializer for learning paths."""

    courses_count = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    class Meta:
        model = LearningPath
        fields = [
            'id', 'title', 'description', 'user', 'courses',
            'courses_count', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_courses(self, obj):
        return [
            {'id': str(course.id), 'title': course.title, 'slug': course.slug}
            for course in obj.courses.all()
        ]

    def get_courses_count(self, obj):
        return obj.courses.count()


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for recommendations."""

    class Meta:
        model = Recommendation
        fields = [
            'id', 'user', 'content_type', 'content_id', 'title',
            'description', 'reason', 'confidence_score', 'is_seen',
            'is_acted_upon', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for user activities."""

    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'content_type',
            'content_id', 'duration_seconds', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
