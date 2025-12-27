"""
Template views for student enrollment and dashboard.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.enrollment.models import Enrollment


@login_required
def student_dashboard_view(request):
    """Student dashboard with enrolled courses and progress."""
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course').order_by('-enrolled_at')
    
    context = {
        'enrollments': enrollments,
    }
    
    return render(request, 'student/dashboard.html', context)
