"""
Models for interactive learning tools.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Lesson
from apps.users.models import User
import uuid

User = get_user_model()


class CodeEditor(models.Model):
    """
    Model for code editor functionality.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='code_editors'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='code_editors',
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='code_editors',
        null=True,
        blank=True
    )
    
    # Code editor properties
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, default='python')  # Language for syntax highlighting
    code = models.TextField()  # The actual code content
    solution = models.TextField(blank=True)  # Solution code (for exercises)
    starter_code = models.TextField(blank=True)  # Initial code to start with
    
    # Settings
    allow_run = models.BooleanField(default=True)  # Allow code execution
    allow_save = models.BooleanField(default=True)  # Allow saving
    time_limit = models.IntegerField(default=5)  # Time limit in seconds for execution
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'code_editors'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Flashcard(models.Model):
    """
    Model for flashcard functionality.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='flashcards'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='flashcards',
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='flashcards',
        null=True,
        blank=True
    )
    
    # Flashcard content
    front = models.TextField()  # Question or term
    back = models.TextField()  # Answer or definition
    category = models.CharField(max_length=100, blank=True)  # Category for organization
    
    # Spaced repetition
    difficulty = models.IntegerField(default=0)  # 0-5 scale
    next_review = models.DateTimeField(null=True, blank=True)  # Next review date
    last_reviewed = models.DateTimeField(null=True, blank=True)  # Last review date
    times_reviewed = models.IntegerField(default=0)  # Number of times reviewed
    correct_answers = models.IntegerField(default=0)  # Number of correct answers
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'flashcards'
        ordering = ['category', '-updated_at']
    
    def __str__(self):
        return f"Flashcard: {self.front[:30]}... - {self.user.username}"


class FlashcardDeck(models.Model):
    """
    Model for organizing flashcards into decks.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='flashcard_decks'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='flashcard_decks',
        null=True,
        blank=True
    )
    
    # Deck properties
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Stats
    total_cards = models.IntegerField(default=0)
    mastered_cards = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'flashcard_decks'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Deck: {self.name} - {self.user.username}"


class Whiteboard(models.Model):
    """
    Model for collaborative whiteboard functionality.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='whiteboards'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='whiteboards',
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='whiteboards',
        null=True,
        blank=True
    )
    
    # Whiteboard properties
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()  # JSON or SVG content
    is_public = models.BooleanField(default=False)  # Allow others to view
    allow_collaboration = models.BooleanField(default=False)  # Allow others to edit
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'whiteboards'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Whiteboard: {self.title} - {self.user.username}"


class InteractiveSession(models.Model):
    """
    Model for tracking interactive learning sessions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='interactive_sessions'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='interactive_sessions',
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='interactive_sessions',
        null=True,
        blank=True
    )
    
    # Session properties
    SESSION_TYPES = [
        ('code_editor', 'Code Editor'),
        ('flashcard', 'Flashcard Review'),
        ('whiteboard', 'Whiteboard'),
        ('quiz', 'Interactive Quiz'),
    ]
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    duration_seconds = models.IntegerField(default=0)  # Session duration in seconds
    interactions_count = models.IntegerField(default=0)  # Number of interactions
    engagement_score = models.FloatField(default=0.0)  # Engagement metric
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'interactive_sessions'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.session_type} session - {self.user.username}"