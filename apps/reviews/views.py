"""
Views for reviews app.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Review
from apps.courses.models import Course
from apps.enrollment.models import Enrollment
from apps.payments.models import PaymentTransaction
from .serializers import ReviewSerializer, ReviewCreateUpdateSerializer
from apps.users.permissions import IsStudent


class ReviewListView(generics.ListAPIView):
    """List reviews for a course."""
    
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Review.objects.filter(course_id=course_id).select_related('student')
        return Review.objects.none()


class ReviewCreateView(generics.CreateAPIView):
    """Create a review for a course."""
    
    serializer_class = ReviewCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    
    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        
        if not course_id:
            return Response({
                'error': 'course_id is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        course = get_object_or_404(Course, id=course_id)
        
        # Check if already reviewed
        if Review.objects.filter(student=request.user, course=course).exists():
            return Response({
                'error': 'You have already reviewed this course.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if enrolled
        enrollment = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).first()
        
        if not enrollment:
            return Response({
                'error': 'You must be enrolled in this course to leave a review.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if verified purchase
        is_verified = False
        if not course.is_free:
            is_verified = PaymentTransaction.objects.filter(
                user=request.user,
                course=course,
                status='completed'
            ).exists()
        else:
            is_verified = True
        
        review = serializer.save(
            student=request.user,
            course=course,
            is_verified_purchase=is_verified
        )
        
        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )


class ReviewUpdateView(generics.UpdateAPIView):
    """Update a review."""
    
    serializer_class = ReviewCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        return Review.objects.filter(student=self.request.user)


class ReviewDeleteView(generics.DestroyAPIView):
    """Delete a review."""
    
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get_queryset(self):
        return Review.objects.filter(student=self.request.user)
