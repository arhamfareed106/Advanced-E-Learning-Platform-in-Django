"""
Models for the gamification system.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Lesson
from apps.quizzes.models import Quiz
import uuid

User = get_user_model()


class Badge(models.Model):
    """
    Badge model for achievements.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Badge info
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)  # CSS class name for icon
    color = models.CharField(max_length=20, default='blue')  # Tailwind color class
    
    # Criteria
    points_required = models.IntegerField(default=0)
    courses_required = models.IntegerField(default=0)
    lessons_completed = models.IntegerField(default=0)
    quizzes_passed = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'badges'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """
    User's earned badges.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_badges'
    )
    badge = models.ForeignKey(
        Badge, 
        on_delete=models.CASCADE, 
        related_name='user_badges'
    )
    
    # Timestamps
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_badges'
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class Achievement(models.Model):
    """
    Achievement model for specific accomplishments.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='achievements'
    )
    
    # Achievement details
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    points = models.IntegerField(default=10)  # Points awarded
    
    # Achievement type
    ACHIEVEMENT_TYPES = [
        ('course_completion', 'Course Completion'),
        ('quiz_mastery', 'Quiz Mastery'),
        ('streak', 'Learning Streak'),
        ('enrollment', 'Course Enrollment'),
        ('review', 'Review Submission'),
        ('social', 'Social Interaction'),
    ]
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    
    # Related objects
    course = models.ForeignKey(
        Course, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='achievements'
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='achievements'
    )
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='achievements'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'achievements'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Leaderboard(models.Model):
    """
    Leaderboard for tracking user rankings.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Ranking info
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='leaderboard_entries'
    )
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    rank = models.IntegerField(default=0)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['-points', 'last_updated']
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level} ({self.points} pts)"


class PointsTransaction(models.Model):
    """
    Track points transactions for audit trail.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='points_transactions'
    )
    
    # Transaction details
    TRANSACTION_TYPES = [
        ('achievement', 'Achievement'),
        ('course_completion', 'Course Completion'),
        ('lesson_completion', 'Lesson Completion'),
        ('quiz_completion', 'Quiz Completion'),
        ('review_submission', 'Review Submission'),
        ('streak_bonus', 'Streak Bonus'),
        ('referral', 'Referral'),
        ('penalty', 'Penalty'),
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    points = models.IntegerField()  # Can be negative for penalties
    description = models.TextField()
    
    # Related objects
    course = models.ForeignKey(
        Course, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'points_transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} ({self.points:+d})"


class LearningStreak(models.Model):
    """
    Track user's learning streaks.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='learning_streaks'
    )
    
    # Streak info
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'learning_streaks'
    
    def __str__(self):
        return f"{self.user.username} - Current: {self.current_streak} days"