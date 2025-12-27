"""
Enrollment and progress tracking models.
"""

from django.db import models
from apps.users.models import User
from apps.courses.models import Course, Lesson
import uuid


class Enrollment(models.Model):
    """Student enrollment in a course."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='enrollments',
        limit_choices_to={'role': 'student'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Progress tracking
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    enrolled_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'enrollments'
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['-enrolled_at']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
    
    def update_progress(self):
        """Calculate and update progress percentage."""
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            self.progress_percentage = 0
        else:
            completed_lessons = self.lesson_progress.filter(is_completed=True).count()
            self.progress_percentage = (completed_lessons / total_lessons) * 100
            
            if self.progress_percentage >= 100:
                self.is_completed = True
                if not self.completed_at:
                    from django.utils import timezone
                    self.completed_at = timezone.now()
        
        self.save()


class LessonProgress(models.Model):
    """Track individual lesson completion."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(
        Enrollment, 
        on_delete=models.CASCADE, 
        related_name='lesson_progress'
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    # Progress
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    watch_time_seconds = models.IntegerField(default=0)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lesson_progress'
        unique_together = ['enrollment', 'lesson']
        ordering = ['enrollment', 'lesson__order']
        indexes = [
            models.Index(fields=['enrollment', 'lesson']),
        ]
    
    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}"
    
    def mark_complete(self):
        """Mark lesson as completed and update enrollment progress."""
        if not self.is_completed:
            from django.utils import timezone
            self.is_completed = True
            self.completed_at = timezone.now()
            self.save()
            self.enrollment.update_progress()
