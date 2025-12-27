"""
Views for enrollment app.
"""

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Enrollment, LessonProgress
from apps.courses.models import Course, Lesson
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer, LessonProgressSerializer
from apps.users.permissions import IsStudent


class EnrollmentListView(generics.ListAPIView):
    """List all enrollments for the current user."""
    
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user).select_related('course')


class EnrollmentCreateView(views.APIView):
    """Enroll in a course."""
    
    permission_classes = [IsAuthenticated, IsStudent]
    
    def post(self, request):
        serializer = EnrollmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        course_id = serializer.validated_data['course_id']
        course = get_object_or_404(Course, id=course_id, status='published')
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({
                'error': 'You are already enrolled in this course.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # For paid courses, check if payment exists
        if not course.is_free:
            from apps.payments.models import PaymentTransaction
            has_paid = PaymentTransaction.objects.filter(
                user=request.user,
                course=course,
                status='completed'
            ).exists()
            
            if not has_paid:
                return Response({
                    'error': 'Payment required for this course.'
                }, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course
        )
        
        # Update course enrollment count
        course.enrollment_count += 1
        course.save(update_fields=['enrollment_count'])
        
        return Response(
            EnrollmentSerializer(enrollment).data,
            status=status.HTTP_201_CREATED
        )


class LessonProgressUpdateView(views.APIView):
    """Update lesson progress."""
    
    permission_classes = [IsAuthenticated, IsStudent]
    
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        
        # Get or create enrollment
        try:
            enrollment = Enrollment.objects.get(
                student=request.user,
                course=lesson.course
            )
        except Enrollment.DoesNotExist:
            return Response({
                'error': 'You are not enrolled in this course.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get or create lesson progress
        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson
        )
        
        # Update progress
        watch_time = request.data.get('watch_time_seconds', 0)
        mark_complete = request.data.get('mark_complete', False)
        
        if watch_time:
            progress.watch_time_seconds = watch_time
        
        if mark_complete and not progress.is_completed:
            progress.mark_complete()
        
        progress.save()
        
        return Response(LessonProgressSerializer(progress).data)


class EnrollmentDetailView(generics.RetrieveAPIView):
    """Get enrollment details with progress."""
    
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)
