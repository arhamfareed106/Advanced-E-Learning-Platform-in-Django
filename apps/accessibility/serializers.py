"""
Serializers for accessibility app.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AccessibilityPreference, WCAGCompliance, AccessibilityFeedback, AccessibilityFeature

User = get_user_model()


class AccessibilityPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for accessibility preferences."""

    class Meta:
        model = AccessibilityPreference
        fields = [
            'id', 'user', 'high_contrast_mode', 'dyslexia_friendly_font',
            'text_size', 'reduce_motion', 'screen_reader_mode',
            'captions_enabled', 'audio_description_enabled', 'transcript_language',
            'simplify_interface', 'break_reminders', 'reading_support',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class WCAGComplianceSerializer(serializers.ModelSerializer):
    """Serializer for WCAG compliance."""

    class Meta:
        model = WCAGCompliance
        fields = [
            'id', 'content_type', 'content_id', 'level_a', 'level_aa',
            'level_aaa', 'perceivable', 'operable', 'understandable',
            'robust', 'compliance_score', 'last_audit_date',
            'next_audit_date', 'compliance_notes'
        ]
        read_only_fields = ['id', 'last_audit_date']


class AccessibilityFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for accessibility feedback."""

    user = serializers.SerializerMethodField()

    class Meta:
        model = AccessibilityFeedback
        fields = [
            'id', 'user', 'content_type', 'content_id', 'issue_type',
            'severity', 'description', 'suggested_solution', 'is_resolved',
            'resolved_at', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'resolved_at']

    def get_user(self, obj):
        if obj.user:
            return {
                'id': str(obj.user.id),
                'username': obj.user.username,
                'email': obj.user.email
            }
        return None


class AccessibilityFeatureSerializer(serializers.ModelSerializer):
    """Serializer for accessibility features."""

    class Meta:
        model = AccessibilityFeature
        fields = [
            'id', 'name', 'description', 'is_enabled',
            'implementation_date', 'last_updated', 'compliance_standards'
        ]
        read_only_fields = ['id', 'implementation_date', 'last_updated']
