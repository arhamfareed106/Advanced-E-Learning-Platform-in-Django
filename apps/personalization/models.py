from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Lesson
from apps.quizzes.models import Quiz
import uuid

User = get_user_model()


class UserPreference(models.Model):
    """
    Model for storing user preferences for personalization.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    learning_style = models.CharField(
        max_length=20,
        choices=[
            ('visual', 'Visual'),
            ('auditory', 'Auditory'),
            ('kinesthetic', 'Kinesthetic'),
            ('reading', 'Reading/Writing'),
        ],
        default='visual'
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='intermediate'
    )
    preferred_language = models.CharField(max_length=10, default='en')
    study_time_preference = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('night', 'Night'),
        ],
        default='morning'
    )
    notification_frequency = models.CharField(
        max_length=20,
        choices=[
            ('frequent', 'Frequent'),
            ('moderate', 'Moderate'),
            ('minimal', 'Minimal'),
        ],
        default='moderate'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s preferences'"


class LearningPath(models.Model):
    """
    Model for defining personalized learning paths.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    courses = models.ManyToManyField(Course, related_name='learning_paths', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Recommendation(models.Model):
    """
    Model for storing personalized recommendations.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    content_type = models.CharField(max_length=20, choices=[
        ('course', 'Course'),
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('resource', 'Resource'),
    ])
    content_id = models.UUIDField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reason = models.TextField(blank=True)  # Why this recommendation was made
    confidence_score = models.FloatField(default=0.0)  # How confident the system is in this recommendation
    is_seen = models.BooleanField(default=False)
    is_acted_upon = models.BooleanField(default=False)  # Whether the user acted on the recommendation
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.title}"


class UserActivity(models.Model):
    """
    Model for tracking user activities for personalization.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=[
        ('course_enrollment', 'Course Enrollment'),
        ('lesson_completion', 'Lesson Completion'),
        ('quiz_attempt', 'Quiz Attempt'),
        ('content_view', 'Content View'),
        ('search', 'Search'),
        ('discussion_participation', 'Discussion Participation'),
        ('resource_download', 'Resource Download'),
    ])
    content_type = models.CharField(max_length=20, choices=[
        ('course', 'Course'),
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('discussion', 'Discussion'),
        ('resource', 'Resource'),
    ], null=True, blank=True)
    content_id = models.UUIDField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)  # How long the activity lasted
    metadata = models.JSONField(default=dict)  # Additional data about the activity
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"