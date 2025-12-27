"""
Admin configuration for quizzes app.
"""

from django.contrib import admin
from .models import Quiz, Question, Answer, Attempt


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    fields = ['answer_text', 'is_correct', 'order']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question_text', 'question_type', 'points', 'order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'time_limit_minutes', 'passing_score', 'is_final_quiz', 'total_questions', 'created_at']
    list_filter = ['is_final_quiz', 'created_at', 'course']
    search_fields = ['title', 'course__title']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text', 'quiz__title']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer_text', 'is_correct', 'order']
    list_filter = ['is_correct']
    search_fields = ['answer_text', 'question__question_text']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'passed', 'started_at', 'submitted_at']
    list_filter = ['passed', 'started_at']
    search_fields = ['student__username', 'quiz__title']
    readonly_fields = ['score', 'total_points', 'earned_points', 'passed', 'started_at', 'submitted_at']
