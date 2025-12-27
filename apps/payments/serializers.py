"""
Serializers for payments app.
"""

from rest_framework import serializers
from .models import PaymentTransaction
from apps.courses.serializers import CourseListSerializer


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """Serializer for payment transactions."""
    
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'course', 'payment_type', 'amount', 'currency',
            'status', 'description', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'completed_at']
