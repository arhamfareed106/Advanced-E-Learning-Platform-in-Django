"""
Certificate model for course completion.
"""

from django.db import models
from apps.users.models import User
from apps.courses.models import Course
import uuid


class Certificate(models.Model):
    """Certificate awarded upon course completion."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='certificates',
        limit_choices_to={'role': 'student'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    
    # Certificate details
    certificate_id = models.CharField(max_length=50, unique=True, editable=False)
    student_name = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    instructor_name = models.CharField(max_length=200)
    completion_date = models.DateField(auto_now_add=True)
    
    # PDF file
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    # Verification
    verification_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'certificates'
        unique_together = ['student', 'course']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['certificate_id']),
            models.Index(fields=['student', 'course']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.certificate_id:
            # Generate unique certificate ID
            import random
            import string
            prefix = 'CERT'
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            self.certificate_id = f"{prefix}-{random_part}"
        
        if not self.student_name:
            self.student_name = f"{self.student.first_name} {self.student.last_name}".strip() or self.student.username
        
        if not self.course_name:
            self.course_name = self.course.title
        
        if not self.instructor_name:
            instructor = self.course.instructor
            self.instructor_name = f"{instructor.first_name} {instructor.last_name}".strip() or instructor.username
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Certificate: {self.student_name} - {self.course_name}"
