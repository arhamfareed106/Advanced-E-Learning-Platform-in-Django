from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Lesson
from apps.quizzes.models import Quiz
import uuid

User = get_user_model()


class AnalyticsReport(models.Model):
    """
    Model for storing analytics reports.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    report_type = models.CharField(max_length=50, choices=[
        ('user_engagement', 'User Engagement'),
        ('course_performance', 'Course Performance'),
        ('learning_progress', 'Learning Progress'),
        ('revenue', 'Revenue'),
        ('instructor', 'Instructor Analytics'),
        ('system_usage', 'System Usage'),
    ])
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # Store the actual analytics data
    filters = models.JSONField(default=dict)  # Store filters used to generate the report
    is_published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return self.title


class UserBehaviorTracking(models.Model):
    """
    Model for tracking detailed user behavior.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behavior_tracking')
    event_type = models.CharField(max_length=50, choices=[
        ('page_view', 'Page View'),
        ('video_play', 'Video Play'),
        ('video_pause', 'Video Pause'),
        ('video_complete', 'Video Complete'),
        ('quiz_start', 'Quiz Start'),
        ('quiz_complete', 'Quiz Complete'),
        ('resource_download', 'Resource Download'),
        ('discussion_post', 'Discussion Post'),
        ('comment_add', 'Comment Add'),
        ('search_perform', 'Search Perform'),
        ('navigation', 'Navigation'),
    ])
    content_type = models.CharField(max_length=20, choices=[
        ('course', 'Course'),
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('discussion', 'Discussion'),
        ('resource', 'Resource'),
        ('page', 'Page'),
    ], null=True, blank=True)
    content_id = models.UUIDField(null=True, blank=True)
    page_url = models.URLField(max_length=500, null=True, blank=True)
    referrer_url = models.URLField(max_length=500, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    duration_seconds = models.FloatField(null=True, blank=True)  # For events that have duration
    metadata = models.JSONField(default=dict)  # Additional event-specific data
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['event_type', '-timestamp']),
            models.Index(fields=['content_type', 'content_id']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.timestamp}"


class LearningAnalytics(models.Model):
    """
    Model for storing learning analytics metrics.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_analytics')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='learning_analytics', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='learning_analytics', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='learning_analytics', null=True, blank=True)
    
    # Engagement metrics
    time_spent_seconds = models.IntegerField(default=0)
    page_views = models.IntegerField(default=0)
    video_views = models.IntegerField(default=0)
    video_completion_rate = models.FloatField(default=0.0)  # 0-100 percentage
    quiz_attempts = models.IntegerField(default=0)
    quiz_average_score = models.FloatField(default=0.0)  # 0-100 percentage
    
    # Learning progress
    course_completion_rate = models.FloatField(default=0.0)  # 0-100 percentage
    lessons_completed = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    assignments_completed = models.IntegerField(default=0)
    total_assignments = models.IntegerField(default=0)
    
    # Social metrics
    discussions_participated = models.IntegerField(default=0)
    comments_made = models.IntegerField(default=0)
    resources_shared = models.IntegerField(default=0)
    
    # Performance metrics
    performance_score = models.FloatField(default=0.0)  # Overall performance score
    engagement_score = models.FloatField(default=0.0)  # Engagement score
    improvement_rate = models.FloatField(default=0.0)  # Rate of improvement
    
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'course', 'lesson', 'quiz')
        ordering = ['-calculated_at']

    def __str__(self):
        return f"Analytics for {self.user.username}"


class DashboardWidget(models.Model):
    """
    Model for storing dashboard widget configurations.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=50, choices=[
        ('line_chart', 'Line Chart'),
        ('bar_chart', 'Bar Chart'),
        ('pie_chart', 'Pie Chart'),
        ('metric_card', 'Metric Card'),
        ('table', 'Table'),
        ('progress', 'Progress'),
    ])
    data_source = models.CharField(max_length=100, help_text="The API endpoint or data source for the widget")
    configuration = models.JSONField(default=dict)  # Widget-specific configuration
    position = models.IntegerField(default=0)  # Position in the dashboard
    width = models.IntegerField(default=4)  # Width in grid units (12 total)
    height = models.IntegerField(default=4)  # Height in grid units
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets', null=True, blank=True)
    
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title