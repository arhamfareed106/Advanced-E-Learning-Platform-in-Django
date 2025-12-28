from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Sum, F
from apps.analytics.models import AnalyticsReport, UserBehaviorTracking, LearningAnalytics, DashboardWidget
from apps.analytics.serializers import (
    AnalyticsReportSerializer, UserBehaviorTrackingSerializer, 
    LearningAnalyticsSerializer, DashboardWidgetSerializer
)
from apps.courses.models import Course, Lesson
from apps.users.models import User


class AnalyticsReportListCreateView(generics.ListCreateAPIView):
    """
    List all analytics reports or create a new report.
    """
    serializer_class = AnalyticsReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AnalyticsReport.objects.filter(generated_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)


class AnalyticsReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific analytics report.
    """
    serializer_class = AnalyticsReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AnalyticsReport.objects.filter(generated_by=self.request.user)


class UserBehaviorTrackingListCreateView(generics.ListCreateAPIView):
    """
    List all user behavior tracking records or create a new record.
    """
    serializer_class = UserBehaviorTrackingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserBehaviorTracking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def track_user_behavior(request):
    """
    Track user behavior event.
    """
    serializer = UserBehaviorTrackingSerializer(
        data=request.data, 
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearningAnalyticsListView(generics.ListAPIView):
    """
    List learning analytics for the user.
    """
    serializer_class = LearningAnalyticsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningAnalytics.objects.filter(user=self.request.user)


class LearningAnalyticsDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update specific learning analytics.
    """
    serializer_class = LearningAnalyticsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningAnalytics.objects.filter(user=self.request.user)


class DashboardWidgetListCreateView(generics.ListCreateAPIView):
    """
    List all dashboard widgets or create a new widget.
    """
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DashboardWidget.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DashboardWidgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific dashboard widget.
    """
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DashboardWidget.objects.filter(owner=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_analytics_summary(request):
    """
    Get user's analytics summary.
    """
    user = request.user
    
    # Get user's learning analytics
    learning_analytics = LearningAnalytics.objects.filter(user=user)
    
    # Calculate overall metrics
    total_courses = learning_analytics.values('course').distinct().count()
    avg_completion_rate = learning_analytics.aggregate(
        avg_completion=Avg('course_completion_rate')
    )['avg_completion'] or 0.0
    
    avg_performance = learning_analytics.aggregate(
        avg_performance=Avg('performance_score')
    )['avg_performance'] or 0.0
    
    avg_engagement = learning_analytics.aggregate(
        avg_engagement=Avg('engagement_score')
    )['avg_engagement'] or 0.0
    
    # Get recent activity
    recent_activities = UserBehaviorTracking.objects.filter(
        user=user
    ).order_by('-timestamp')[:10]
    
    # Get user's enrolled courses
    enrolled_courses = Course.objects.filter(enrollments__user=user)
    
    return Response({
        'summary': {
            'total_courses_enrolled': enrolled_courses.count(),
            'average_completion_rate': avg_completion_rate,
            'average_performance': avg_performance,
            'average_engagement': avg_engagement,
            'total_learning_hours': learning_analytics.aggregate(
                total_time=Sum('time_spent_seconds')
            )['total_time'] or 0,
        },
        'recent_activities': UserBehaviorTrackingSerializer(recent_activities, many=True).data,
        'course_progress': [
            {
                'course_id': la.course.id,
                'course_title': la.course.title,
                'completion_rate': la.course_completion_rate,
                'performance': la.performance_score
            }
            for la in learning_analytics.filter(course__isnull=False)[:5]
        ]
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_platform_analytics(request):
    """
    Get platform-wide analytics for instructors/admins.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {'error': 'Permission denied'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get platform metrics
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()
    
    # Get engagement metrics
    total_learning_time = LearningAnalytics.objects.aggregate(
        total_time=Sum('time_spent_seconds')
    )['total_time'] or 0
    
    avg_completion_rate = LearningAnalytics.objects.aggregate(
        avg_completion=Avg('course_completion_rate')
    )['avg_completion'] or 0.0
    
    # Get recent user activity
    recent_activities = UserBehaviorTracking.objects.order_by('-timestamp')[:20]
    
    return Response({
        'platform_metrics': {
            'total_users': total_users,
            'total_courses': total_courses,
            'total_lessons': total_lessons,
            'total_learning_hours': total_learning_time / 3600,  # Convert to hours
            'average_completion_rate': avg_completion_rate,
        },
        'recent_activities': UserBehaviorTrackingSerializer(recent_activities, many=True).data
    }, status=status.HTTP_200_OK)