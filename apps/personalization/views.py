from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.personalization.models import UserPreference, LearningPath, Recommendation, UserActivity
from apps.personalization.serializers import (
    UserPreferenceSerializer, LearningPathSerializer, 
    RecommendationSerializer, UserActivitySerializer
)


class UserPreferenceDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user preferences.
    """
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_preference, created = UserPreference.objects.get_or_create(user=self.request.user)
        return user_preference


class LearningPathListCreateView(generics.ListCreateAPIView):
    """
    List all learning paths for the user or create a new learning path.
    """
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningPath.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LearningPathDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific learning path.
    """
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningPath.objects.filter(user=self.request.user)


class RecommendationListView(generics.ListAPIView):
    """
    List all recommendations for the user.
    """
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user).order_by('-created_at')


class RecommendationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific recommendation.
    """
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_recommendation_seen(request, recommendation_id):
    """
    Mark a recommendation as seen.
    """
    try:
        recommendation = get_object_or_404(Recommendation, id=recommendation_id, user=request.user)
        recommendation.is_seen = True
        recommendation.save()
        return Response({'message': 'Recommendation marked as seen'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_recommendation_acted_upon(request, recommendation_id):
    """
    Mark a recommendation as acted upon.
    """
    try:
        recommendation = get_object_or_404(Recommendation, id=recommendation_id, user=request.user)
        recommendation.is_acted_upon = True
        recommendation.save()
        return Response({'message': 'Recommendation marked as acted upon'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserActivityListCreateView(generics.ListCreateAPIView):
    """
    List all user activities or create a new user activity.
    """
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_user_activity(request):
    """
    Track a user activity for personalization.
    """
    serializer = UserActivitySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_personalized_recommendations(request):
    """
    Get personalized recommendations based on user activity and preferences.
    """
    # In a real implementation, this would use ML algorithms to generate recommendations
    # For now, we'll return a mock response based on user's learning path
    user = request.user
    preferences = UserPreference.objects.filter(user=user).first()
    
    # Get user's learning paths
    learning_paths = LearningPath.objects.filter(user=user)
    
    # Get user's recent activities
    recent_activities = UserActivity.objects.filter(user=user).order_by('-created_at')[:10]
    
    # Mock recommendations based on recent activities
    mock_recommendations = []
    for activity in recent_activities:
        if activity.content_type == 'course_enrollment':
            mock_recommendations.append({
                'id': activity.id,
                'title': f'Similar course to {activity.metadata.get("course_title", "your recent course")}',
                'description': 'Based on your interest in this topic',
                'content_type': 'course',
                'confidence_score': 0.8
            })
    
    return Response({
        'recommendations': mock_recommendations,
        'learning_style': preferences.learning_style if preferences else 'visual',
        'next_steps': ['Complete your current course', 'Try a related quiz', 'Join a study group']
    }, status=status.HTTP_200_OK)