from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.accessibility.models import AccessibilityPreference, WCAGCompliance, AccessibilityFeedback, AccessibilityFeature
from apps.accessibility.serializers import (
    AccessibilityPreferenceSerializer, WCAGComplianceSerializer, 
    AccessibilityFeedbackSerializer, AccessibilityFeatureSerializer
)


class AccessibilityPreferenceDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user accessibility preferences.
    """
    serializer_class = AccessibilityPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_preference, created = AccessibilityPreference.objects.get_or_create(user=self.request.user)
        return user_preference


class WCAGComplianceListView(generics.ListAPIView):
    """
    List WCAG compliance records.
    """
    serializer_class = WCAGComplianceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        content_id = self.request.query_params.get('content_id')
        
        queryset = WCAGCompliance.objects.all()
        
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        if content_id:
            queryset = queryset.filter(content_id=content_id)
            
        return queryset


class WCAGComplianceDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a specific WCAG compliance record.
    """
    serializer_class = WCAGComplianceSerializer
    permission_classes = [IsAuthenticated]
    queryset = WCAGCompliance.objects.all()


class AccessibilityFeedbackListCreateView(generics.ListCreateAPIView):
    """
    List all accessibility feedback or create new feedback.
    """
    serializer_class = AccessibilityFeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AccessibilityFeedback.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccessibilityFeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific accessibility feedback.
    """
    serializer_class = AccessibilityFeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AccessibilityFeedback.objects.filter(user=self.request.user)


class AccessibilityFeatureListView(generics.ListAPIView):
    """
    List all accessibility features.
    """
    serializer_class = AccessibilityFeatureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AccessibilityFeature.objects.filter(is_enabled=True)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_accessibility_feedback(request):
    """
    Submit accessibility feedback.
    """
    serializer = AccessibilityFeedbackSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_accessibility_profile(request):
    """
    Get user's complete accessibility profile.
    """
    # Get user's accessibility preferences
    preferences, created = AccessibilityPreference.objects.get_or_create(user=request.user)
    
    # Get user's accessibility feedback
    feedback = AccessibilityFeedback.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get platform accessibility features
    features = AccessibilityFeature.objects.filter(is_enabled=True)
    
    return Response({
        'preferences': AccessibilityPreferenceSerializer(preferences).data,
        'recent_feedback': AccessibilityFeedbackSerializer(feedback, many=True).data,
        'platform_features': AccessibilityFeatureSerializer(features, many=True).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wcag_compliance_summary(request):
    """
    Get WCAG compliance summary for the platform.
    """
    total_content = WCAGCompliance.objects.count()
    level_a_content = WCAGCompliance.objects.filter(level_a=True).count()
    level_aa_content = WCAGCompliance.objects.filter(level_aa=True).count()
    level_aaa_content = WCAGCompliance.objects.filter(level_aaa=True).count()
    
    avg_compliance_score = WCAGCompliance.objects.aggregate(
        avg_score=models.Avg('compliance_score')
    )['avg_score'] or 0.0
    
    return Response({
        'total_content': total_content,
        'level_a_compliance': {
            'count': level_a_content,
            'percentage': total_content > 0 and (level_a_content / total_content) * 100 or 0
        },
        'level_aa_compliance': {
            'count': level_aa_content,
            'percentage': total_content > 0 and (level_aa_content / total_content) * 100 or 0
        },
        'level_aaa_compliance': {
            'count': level_aaa_content,
            'percentage': total_content > 0 and (level_aaa_content / total_content) * 100 or 0
        },
        'average_compliance_score': avg_compliance_score
    }, status=status.HTTP_200_OK)