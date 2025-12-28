from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.accessibility.models import AccessibilityPreference, WCAGCompliance, AccessibilityFeedback, AccessibilityFeature

User = get_user_model()


class AccessibilityPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for AccessibilityPreference model.
    """
    class Meta:
        model = AccessibilityPreference
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class WCAGComplianceSerializer(serializers.ModelSerializer):
    """
    Serializer for WCAGCompliance model.
    """
    class Meta:
        model = WCAGCompliance
        fields = '__all__'
        read_only_fields = ('id', 'last_audit_date')


class AccessibilityFeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for AccessibilityFeedback model.
    """
    class Meta:
        model = AccessibilityFeedback
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'resolved_at')

    def create(self, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        validated_data['user'] = user
        return super().create(validated_data)


class AccessibilityFeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for AccessibilityFeature model.
    """
    class Meta:
        model = AccessibilityFeature
        fields = '__all__'
        read_only_fields = ('id', 'implementation_date', 'last_updated')