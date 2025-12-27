"""
Serializers for courses app.
"""

from rest_framework import serializers
from .models import Category, Course, Lesson
from apps.users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category model."""
    
    course_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'course_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_course_count(self, obj):
        return obj.courses.filter(status='published').count()


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for lesson model."""
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'lesson_type', 'chapter_number',
            'order', 'video_url', 'video_file', 'document_file', 'content',
            'duration_minutes', 'is_preview', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for course list view."""
    
    instructor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail', 'preview_video',
            'price', 'is_free', 'difficulty', 'status', 'instructor', 'category',
            'duration_hours', 'language', 'enrollment_count', 'average_rating',
            'review_count', 'total_lessons', 'created_at', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'enrollment_count', 'average_rating', 'review_count']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer for course detail view."""
    
    instructor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail', 'preview_video',
            'price', 'is_free', 'difficulty', 'status', 'instructor', 'category',
            'duration_hours', 'language', 'requirements', 'what_you_will_learn',
            'enrollment_count', 'average_rating', 'review_count', 'lessons',
            'total_lessons', 'total_duration_minutes', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'enrollment_count', 'average_rating', 'review_count']


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating courses."""
    
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'category', 'thumbnail', 'preview_video',
            'price', 'difficulty', 'status', 'duration_hours', 'language',
            'requirements', 'what_you_will_learn'
        ]
    
    def create(self, validated_data):
        # Set instructor from request user
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)
