"""
Template views for courses app.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from ..courses.models import Course, Category


def course_list_view(request):
    """Course listing page with filters."""
    courses = Course.objects.filter(status='published').select_related('instructor', 'category')
    
    # Get categories for filter dropdown
    categories = Category.objects.all()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        courses = courses.filter(difficulty=difficulty)
    
    # Filter by price
    if request.GET.get('free'):
        courses = courses.filter(price=0)
    elif request.GET.get('paid'):
        courses = courses.filter(price__gt=0)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    if sort:
        courses = courses.order_by(sort)
    
    # Pagination
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page', 1)
    courses_page = paginator.get_page(page_number)
    
    context = {
        'courses': courses_page,
        'categories': categories,
    }
    
    return render(request, 'courses/course_list.html', context)


def course_detail_view(request, slug):
    """Course detail page."""
    course = get_object_or_404(
        Course.objects.select_related('instructor', 'category').prefetch_related('lessons'),
        slug=slug,
        status='published'
    )
    
    # Get related courses
    related_courses = Course.objects.filter(
        category=course.category,
        status='published'
    ).exclude(id=course.id)[:4]
    
    context = {
        'course': course,
        'related_courses': related_courses,
    }
    
    return render(request, 'courses/course_detail.html', context)
