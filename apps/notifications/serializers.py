"""
Serializers for notifications app.
"""

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message',
            'action_url', 'is_read', 'read_at', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']
