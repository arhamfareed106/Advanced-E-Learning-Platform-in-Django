"""
Template views for admin dashboard.
"""

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg
from apps.users.models import User
from apps.courses.models import Course, Category
from apps.enrollment.models import Enrollment
from apps.certificates.models import Certificate


@staff_member_required
def admin_dashboard_view(request):
    """Admin dashboard page."""
    # Get counts
    total_users = User.objects.count()
    total_students = User.objects.filter(role='student').count()
    total_instructors = User.objects.filter(role='instructor').count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    total_certificates = Certificate.objects.count()
    
    # Get recent users
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Get recent courses
    recent_courses = Course.objects.select_related('instructor').order_by('-created_at')[:10]
    
    # Get top courses by enrollment
    top_courses = Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:5]
    
    # Get category distribution
    categories = Category.objects.annotate(
        course_count=Count('courses')
    ).order_by('-course_count')
    
    # Get revenue (if payments exist)
    try:
        from apps.payments.models import PaymentTransaction
        total_revenue = PaymentTransaction.objects.filter(
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
    except:
        total_revenue = 0
    
    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_instructors': total_instructors,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_certificates': total_certificates,
        'total_revenue': total_revenue,
        'recent_users': recent_users,
        'recent_courses': recent_courses,
        'top_courses': top_courses,
        'categories': categories,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)
