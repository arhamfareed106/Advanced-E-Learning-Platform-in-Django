"""
Quiz, Question, Answer, and Attempt models.
"""

from django.db import models
from apps.users.models import User
from apps.courses.models import Course
import uuid


class Quiz(models.Model):
    """Quiz model for course assessments."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    
    # Basic info
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Settings
    time_limit_minutes = models.IntegerField(default=30, help_text="Time limit in minutes, 0 for no limit")
    passing_score = models.IntegerField(default=70, help_text="Passing score percentage")
    randomize_questions = models.BooleanField(default=True)
    show_answers_after_submission = models.BooleanField(default=True)
    is_final_quiz = models.BooleanField(default=False)  # Required for certificate
    
    # Metadata
    max_attempts = models.IntegerField(default=3, help_text="Maximum attempts allowed, 0 for unlimited")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quizzes'
        verbose_name_plural = 'Quizzes'
        ordering = ['course', '-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    @property
    def total_questions(self):
        return self.questions.count()
    
    @property
    def total_points(self):
        return self.questions.aggregate(
            total=models.Sum('points')
        )['total'] or 0


class Question(models.Model):
    """Question model for quizzes."""
    
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    
    # Question content
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='mcq')
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    # Explanation
    explanation = models.TextField(blank=True, help_text="Explanation shown after answer")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['quiz', 'order']
        indexes = [
            models.Index(fields=['quiz', 'order']),
        ]
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class Answer(models.Model):
    """Answer choices for questions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    
    # Answer content
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'answers'
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"{self.question.question_text[:50]} - {self.answer_text[:30]}"


class Attempt(models.Model):
    """Quiz attempt by a student."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='quiz_attempts',
        limit_choices_to={'role': 'student'}
    )
    
    # Attempt data
    answers = models.JSONField(default=dict)  # {question_id: answer_id or answer_text}
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_points = models.IntegerField(default=0)
    earned_points = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_taken_seconds = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'attempts'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['student', 'quiz']),
            models.Index(fields=['-started_at']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - {self.score}%"
    
    def calculate_score(self):
        """Calculate the score based on answers."""
        total_points = 0
        earned_points = 0
        
        for question in self.quiz.questions.all():
            total_points += question.points
            question_id = str(question.id)
            
            if question_id in self.answers:
                student_answer = self.answers[question_id]
                
                if question.question_type in ['mcq', 'true_false']:
                    # Check if selected answer is correct
                    try:
                        answer = question.answers.get(id=student_answer)
                        if answer.is_correct:
                            earned_points += question.points
                    except Answer.DoesNotExist:
                        pass
                elif question.question_type == 'short_answer':
                    # For short answer, check against correct answers (case-insensitive)
                    correct_answers = question.answers.filter(is_correct=True)
                    student_answer_lower = str(student_answer).lower().strip()
                    for correct in correct_answers:
                        if correct.answer_text.lower().strip() == student_answer_lower:
                            earned_points += question.points
                            break
        
        self.total_points = total_points
        self.earned_points = earned_points
        self.score = (earned_points / total_points * 100) if total_points > 0 else 0
        self.passed = self.score >= self.quiz.passing_score
        self.save()
