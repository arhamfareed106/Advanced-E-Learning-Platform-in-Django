"""
Serializers for analytics app.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AnalyticsReport, UserBehaviorTracking, LearningAnalytics, DashboardWidget

User = get_user_model()


class AnalyticsReportSerializer(serializers.ModelSerializer):
    """Serializer for analytics reports."""

    generated_by = serializers.SerializerMethodField()

    class Meta:
        model = AnalyticsReport
        fields = [
            'id', 'title', 'description', 'report_type', 'generated_by',
            'generated_at', 'data', 'filters', 'is_published'
        ]
        read_only_fields = ['id', 'generated_by', 'generated_at']

    def get_generated_by(self, obj):
        return {
            'id': str(obj.generated_by.id),
            'username': obj.generated_by.username,
            'email': obj.generated_by.email
        }


class UserBehaviorTrackingSerializer(serializers.ModelSerializer):
    """Serializer for user behavior tracking."""

    class Meta:
        model = UserBehaviorTracking
        fields = [
            'id', 'user', 'event_type', 'content_type', 'content_id',
            'page_url', 'referrer_url', 'session_id', 'duration_seconds',
            'metadata', 'timestamp'
        ]
        read_only_fields = ['id', 'user', 'timestamp']


class LearningAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for learning analytics."""

    course = serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = LearningAnalytics
        fields = [
            'id', 'user', 'course', 'lesson', 'quiz',
            'time_spent_seconds', 'page_views', 'video_views',
            'video_completion_rate', 'quiz_attempts', 'quiz_average_score',
            'course_completion_rate', 'lessons_completed', 'total_lessons',
            'assignments_completed', 'total_assignments',
            'discussions_participated', 'comments_made', 'resources_shared',
            'performance_score', 'engagement_score', 'improvement_rate',
            'calculated_at'
        ]
        read_only_fields = ['id', 'user', 'calculated_at']

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


class DashboardWidgetSerializer(serializers.ModelSerializer):
    """Serializer for dashboard widgets."""

    owner = serializers.SerializerMethodField()

    class Meta:
        model = DashboardWidget
        fields = [
            'id', 'title', 'widget_type', 'data_source', 'configuration',
            'position', 'width', 'height', 'is_active', 'owner'
        ]
        read_only_fields = ['id', 'owner']

    def get_owner(self, obj):
        if obj.owner:
            return {'id': str(obj.owner.id), 'username': obj.owner.username}
        return None
