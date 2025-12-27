"""
Serializers for enrollment app.
"""

from rest_framework import serializers
from .models import Enrollment, LessonProgress
from apps.courses.serializers import CourseListSerializer, LessonSerializer


class LessonProgressSerializer(serializers.ModelSerializer):
    """Serializer for lesson progress."""
    
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = LessonProgress
        fields = [
            'id', 'lesson', 'is_completed', 'completed_at',
            'watch_time_seconds', 'started_at', 'last_accessed'
        ]
        read_only_fields = ['id', 'started_at', 'last_accessed']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for enrollment."""
    
    course = CourseListSerializer(read_only=True)
    lesson_progress = LessonProgressSerializer(many=True, read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'course', 'progress_percentage', 'is_completed',
            'completed_at', 'enrolled_at', 'last_accessed', 'lesson_progress'
        ]
        read_only_fields = ['id', 'progress_percentage', 'is_completed', 'completed_at', 'enrolled_at', 'last_accessed']


class EnrollmentCreateSerializer(serializers.Serializer):
    """Serializer for creating enrollment."""
    
    course_id = serializers.UUIDField()
