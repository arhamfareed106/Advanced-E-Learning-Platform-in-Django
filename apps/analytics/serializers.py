from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.analytics.models import AnalyticsReport, UserBehaviorTracking, LearningAnalytics, DashboardWidget

User = get_user_model()


class AnalyticsReportSerializer(serializers.ModelSerializer):
    """
    Serializer for AnalyticsReport model.
    """
    class Meta:
        model = AnalyticsReport
        fields = '__all__'
        read_only_fields = ('id', 'generated_by', 'generated_at')


class UserBehaviorTrackingSerializer(serializers.ModelSerializer):
    """
    Serializer for UserBehaviorTracking model.
    """
    class Meta:
        model = UserBehaviorTracking
        fields = '__all__'
        read_only_fields = ('id', 'user', 'timestamp')

    def create(self, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        validated_data['user'] = user
        return super().create(validated_data)


class LearningAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for LearningAnalytics model.
    """
    class Meta:
        model = LearningAnalytics
        fields = '__all__'
        read_only_fields = ('id', 'user', 'calculated_at')


class DashboardWidgetSerializer(serializers.ModelSerializer):
    """
    Serializer for DashboardWidget model.
    """
    class Meta:
        model = DashboardWidget
        fields = '__all__'
        read_only_fields = ('id', 'owner')

    def create(self, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        validated_data['owner'] = user
        return super().create(validated_data)