from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Lesson
import uuid

User = get_user_model()


class AccessibilityPreference(models.Model):
    """
    Model for storing user accessibility preferences.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accessibility_preferences')
    
    # Visual accessibility
    high_contrast_mode = models.BooleanField(default=False)
    dyslexia_friendly_font = models.BooleanField(default=False)
    text_size = models.CharField(
        max_length=10,
        choices=[
            ('small', 'Small'),
            ('normal', 'Normal'),
            ('large', 'Large'),
            ('xlarge', 'Extra Large'),
        ],
        default='normal'
    )
    reduce_motion = models.BooleanField(default=False)
    screen_reader_mode = models.BooleanField(default=False)
    
    # Audio accessibility
    captions_enabled = models.BooleanField(default=True)
    audio_description_enabled = models.BooleanField(default=False)
    transcript_language = models.CharField(max_length=10, default='en')
    
    # Cognitive accessibility
    simplify_interface = models.BooleanField(default=False)
    break_reminders = models.BooleanField(default=True)
    reading_support = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s accessibility preferences"


class WCAGCompliance(models.Model):
    """
    Model for tracking WCAG compliance of content.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Content reference
    content_type = models.CharField(max_length=20, choices=[
        ('course', 'Course'),
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('resource', 'Resource'),
        ('page', 'Page'),
    ])
    content_id = models.UUIDField()
    
    # WCAG levels
    level_a = models.BooleanField(default=False)  # Minimum level
    level_aa = models.BooleanField(default=False)  # Standard level
    level_aaa = models.BooleanField(default=False)  # Enhanced level
    
    # Specific guidelines compliance
    perceivable = models.BooleanField(default=False)
    operable = models.BooleanField(default=False)
    understandable = models.BooleanField(default=False)
    robust = models.BooleanField(default=False)
    
    # Compliance details
    compliance_score = models.FloatField(default=0.0)  # 0-100 percentage
    last_audit_date = models.DateTimeField(auto_now_add=True)
    next_audit_date = models.DateTimeField(null=True, blank=True)
    compliance_notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('content_type', 'content_id')
        ordering = ['-last_audit_date']

    def __str__(self):
        return f"{self.content_type} {self.content_id} - WCAG Compliance"


class AccessibilityFeedback(models.Model):
    """
    Model for collecting accessibility feedback from users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accessibility_feedback', null=True, blank=True)
    content_type = models.CharField(max_length=20, choices=[
        ('course', 'Course'),
        ('lesson', 'Lesson'),
        ('quiz', 'Quiz'),
        ('resource', 'Resource'),
        ('page', 'Page'),
        ('feature', 'Feature'),
    ], null=True, blank=True)
    content_id = models.UUIDField(null=True, blank=True)
    issue_type = models.CharField(max_length=50, choices=[
        ('navigation', 'Navigation'),
        ('color_contrast', 'Color Contrast'),
        ('screen_reader', 'Screen Reader'),
        ('keyboard', 'Keyboard Navigation'),
        ('audio', 'Audio Issues'),
        ('visual', 'Visual Issues'),
        ('cognitive', 'Cognitive'),
        ('other', 'Other'),
    ])
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='medium')
    description = models.TextField()
    suggested_solution = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Accessibility issue: {self.issue_type} - {self.description[:50]}..."


class AccessibilityFeature(models.Model):
    """
    Model for tracking accessibility features implemented in the platform.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_enabled = models.BooleanField(default=True)
    implementation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    compliance_standards = models.JSONField(default=list)  # e.g., ['WCAG 2.1 AA', 'Section 508']
    
    def __str__(self):
        return self.name