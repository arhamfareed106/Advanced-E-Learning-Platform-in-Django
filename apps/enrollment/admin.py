"""
Admin configuration for enrollment app.
"""

from django.contrib import admin
from .models import Enrollment, LessonProgress


class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0
    readonly_fields = ['started_at', 'last_accessed', 'completed_at']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'progress_percentage', 'is_completed', 'enrolled_at']
    list_filter = ['is_completed', 'enrolled_at']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['progress_percentage', 'is_completed', 'completed_at', 'enrolled_at', 'last_accessed']
    inlines = [LessonProgressInline]


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'watch_time_seconds', 'last_accessed']
    list_filter = ['is_completed', 'last_accessed']
    search_fields = ['enrollment__student__username', 'lesson__title']
    readonly_fields = ['started_at', 'last_accessed', 'completed_at']
