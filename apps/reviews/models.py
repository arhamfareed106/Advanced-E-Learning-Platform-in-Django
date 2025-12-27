"""
Review and rating model for courses.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import User
from apps.courses.models import Course
import uuid


class Review(models.Model):
    """Course review and rating."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        limit_choices_to={'role': 'student'}
    )
    
    # Rating and review
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    review_text = models.TextField(blank=True)
    
    # Metadata
    is_verified_purchase = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        unique_together = ['course', 'student']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['course', '-created_at']),
            models.Index(fields=['student']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.rating}★"
