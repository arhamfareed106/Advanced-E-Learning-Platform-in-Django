"""
Template views for courses (non-API views).
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Course, Lesson, Category
from apps.enrollment.models import Enrollment, LessonProgress


def course_catalog_view(request):
    """Course catalog page with search and filters."""
    courses = Course.objects.filter(status='published').select_related('instructor', 'category')
    
    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    # Difficulty filter
    difficulty = request.GET.get('difficulty')
    if difficulty:
        courses = courses.filter(difficulty=difficulty)
    
    # Price filter
    is_free = request.GET.get('is_free')
    if is_free == 'true':
        courses = courses.filter(is_free=True)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    courses = courses.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'is_free_filter': is_free,
        'sort_by': sort_by,
    }
    
    return render(request, 'courses/catalog.html', context)


def course_detail_view(request, slug):
    """Course detail page."""
    course = get_object_or_404(
        Course.objects.select_related('instructor', 'category'),
        slug=slug,
        status='published'
    )
    
    # Get lessons
    lessons = course.lessons.all().order_by('chapter_number', 'order')
    
    # Check if user is enrolled
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()
    
    # Get reviews
    reviews = course.reviews.select_related('student').order_by('-created_at')[:5]
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'reviews': reviews,
    }
    
    return render(request, 'courses/detail.html', context)


@login_required
def lesson_detail_view(request, slug, lesson_id):
    """Lesson viewer page."""
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Check if user is enrolled
    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=course
    )
    
    # Get or create lesson progress
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )
    
    # Get all lessons for navigation
    lessons = course.lessons.all().order_by('chapter_number', 'order')
    
    # Find previous and next lessons
    lesson_list = list(lessons)
    current_index = lesson_list.index(lesson)
    prev_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None
    
    context = {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'lessons': lessons,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
    }
    
    return render(request, 'courses/lesson.html', context)


@login_required
def mark_lesson_complete(request, slug, lesson_id):
    """Mark a lesson as complete."""
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=slug)
        lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
        enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
        
        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson
        )
        
        progress.is_completed = True
        progress.save()
        
        messages.success(request, 'Lesson marked as complete!')
        
        # Redirect to next lesson or course detail
        lessons = list(course.lessons.all().order_by('chapter_number', 'order'))
        current_index = lessons.index(lesson)
        
        if current_index < len(lessons) - 1:
            next_lesson = lessons[current_index + 1]
            return redirect('lesson_detail', slug=slug, lesson_id=next_lesson.id)
        else:
            return redirect('course_detail', slug=slug)
    
    return redirect('course_detail', slug=slug)


@login_required
def enroll_course(request, slug):
    """Enroll in a course."""
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=slug, status='published')
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.info(request, 'You are already enrolled in this course.')
        else:
            # Create enrollment
            Enrollment.objects.create(
                student=request.user,
                course=course
            )
            messages.success(request, f'Successfully enrolled in {course.title}!')
        
        return redirect('course_detail', slug=slug)
    
    return redirect('course_catalog')
