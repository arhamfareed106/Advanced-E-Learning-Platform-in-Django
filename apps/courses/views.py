"""
Views for courses app.
"""

from rest_framework import generics, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Category, Course, Lesson
from .serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer,
    CourseCreateUpdateSerializer, LessonSerializer
)
from apps.users.permissions import IsInstructor, IsInstructorOrAdmin


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for categories."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for courses with search and filtering."""
    
    queryset = Course.objects.filter(status='published').select_related('instructor', 'category')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'is_free']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'average_rating', 'enrollment_count', 'price']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Show all courses for instructors viewing their own
        if self.request.user.is_authenticated and self.request.user.is_instructor:
            if self.request.query_params.get('my_courses'):
                queryset = Course.objects.filter(instructor=self.request.user)
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsInstructor()]
        return [AllowAny()]
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, slug=None):
        """Get all lessons for a course."""
        course = self.get_object()
        lessons = course.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for lessons."""
    
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsInstructorOrAdmin]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset
    
    def perform_create(self, serializer):
        # Ensure the instructor owns the course
        course = serializer.validated_data['course']
        if course.instructor != self.request.user and not self.request.user.is_admin_user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to add lessons to this course.")
        serializer.save()
