from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.personalization.models import UserPreference, LearningPath, Recommendation, UserActivity
from apps.courses.models import Course

User = get_user_model()


class UserPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPreference model.
    """
    class Meta:
        model = UserPreference
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model (used in LearningPath).
    """
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'difficulty_level', 'estimated_duration']
        read_only_fields = ['id']


class LearningPathSerializer(serializers.ModelSerializer):
    """
    Serializer for LearningPath model.
    """
    courses = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = LearningPath
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class RecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for Recommendation model.
    """
    class Meta:
        model = Recommendation
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for UserActivity model.
    """
    class Meta:
        model = UserActivity
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)