"""
Serializers for reviews app.
"""

from rest_framework import serializers
from .models import Review
from apps.users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews."""
    
    student = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'student', 'rating', 'review_text',
            'is_verified_purchase', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'student', 'is_verified_purchase', 'created_at', 'updated_at']


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating reviews."""
    
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
