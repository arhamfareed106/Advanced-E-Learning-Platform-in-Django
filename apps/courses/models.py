"""
Course models for the e-learning platform.
Includes Category, Course, and Lesson models.
"""

from django.db import models
from django.utils.text import slugify
from apps.users.models import User
import uuid


class Category(models.Model):
    """Course category model."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Icon class name
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """Course model with all details."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instructor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='courses_taught',
        limit_choices_to={'role': 'instructor'}
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='courses'
    )
    
    # Basic info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    
    # Media
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    preview_video = models.URLField(blank=True)  # YouTube or direct link
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=True)
    
    # Course details
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Metadata
    duration_hours = models.IntegerField(default=0, help_text="Estimated course duration in hours")
    language = models.CharField(max_length=50, default='English')
    requirements = models.JSONField(default=list, blank=True)  # List of prerequisites
    what_you_will_learn = models.JSONField(default=list, blank=True)  # Learning outcomes
    
    # Stats
    enrollment_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['instructor']),
            models.Index(fields=['-average_rating']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.is_free = (self.price == 0)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def total_lessons(self):
        return self.lessons.count()
    
    @property
    def total_duration_minutes(self):
        return self.lessons.aggregate(
            total=models.Sum('duration_minutes')
        )['total'] or 0


class Lesson(models.Model):
    """Lesson model for course content."""
    
    LESSON_TYPE_CHOICES = [
        ('video', 'Video'),
        ('document', 'Document'),
        ('quiz', 'Quiz'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    
    # Basic info
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='video')
    
    # Ordering
    chapter_number = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    # Content
    video_url = models.URLField(blank=True)  # YouTube or uploaded video
    video_file = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    document_file = models.FileField(upload_to='lesson_documents/', blank=True, null=True)
    content = models.TextField(blank=True)  # Text content or notes
    
    # Metadata
    duration_minutes = models.IntegerField(default=0)
    is_preview = models.BooleanField(default=False)  # Free preview lesson
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lessons'
        ordering = ['course', 'chapter_number', 'order']
        indexes = [
            models.Index(fields=['course', 'chapter_number', 'order']),
        ]
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
