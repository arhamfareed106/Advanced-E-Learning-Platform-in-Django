"""
Admin configuration for courses app.
"""

from django.contrib import admin
from .models import Category, Course, Lesson


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['title', 'lesson_type', 'chapter_number', 'order', 'duration_minutes', 'is_preview']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'price', 'difficulty', 'status', 'enrollment_count', 'average_rating', 'created_at']
    list_filter = ['status', 'difficulty', 'category', 'is_free', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    readonly_fields = ['enrollment_count', 'average_rating', 'review_count']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'lesson_type', 'chapter_number', 'order', 'duration_minutes', 'is_preview']
    list_filter = ['lesson_type', 'is_preview', 'course']
    search_fields = ['title', 'course__title']
