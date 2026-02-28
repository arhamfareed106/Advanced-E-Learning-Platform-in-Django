"""
Template views for student dashboard.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.enrollment.models import Enrollment
from apps.certificates.models import Certificate
from apps.gamification.models import UserBadge, Leaderboard, LearningStreak


@login_required
def student_dashboard_view(request):
    """Student dashboard page."""
    # Get student's enrollments
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')[:5]
    
    # Get certificates
    certificates = Certificate.objects.filter(student=request.user)[:3]
    
    # Get badges
    badges = UserBadge.objects.filter(user=request.user).select_related('badge')[:6]
    
    # Get leaderboard entry
    try:
        leaderboard = Leaderboard.objects.get(user=request.user)
        level = leaderboard.level
        points = leaderboard.points
    except Leaderboard.DoesNotExist:
        level = 1
        points = 0
    
    # Get learning streak
    try:
        streak = LearningStreak.objects.get(user=request.user)
        streak_count = streak.current_streak
    except LearningStreak.DoesNotExist:
        streak_count = 0
    
    # Calculate learning hours (from lesson progress)
    from apps.enrollment.models import LessonProgress
    total_seconds = LessonProgress.objects.filter(
        enrollment__student=request.user
    ).aggregate(total=Sum('watch_time_seconds'))['total'] or 0
    learning_hours = int(total_seconds / 3600)
    
    context = {
        'recent_enrollments': enrollments,
        'certificates_count': certificates.count(),
        'enrollments_count': enrollments.count(),
        'badges_count': badges.count(),
        'recent_badges': badges,
        'level': level,
        'points': points,
        'next_level_points': level * 100,
        'progress_percentage': (points % 100),
        'streak': streak_count,
        'learning_hours': learning_hours,
    }
    
    return render(request, 'student/dashboard.html', context)


@login_required
def my_courses_view(request):
    """Student's enrolled courses page."""
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    context = {
        'enrollments': enrollments,
    }
    
    return render(request, 'student/my_courses.html', context)


@login_required
def certificates_view(request):
    """Student's certificates page."""
    certificates = Certificate.objects.filter(student=request.user).select_related('course')
    
    context = {
        'certificates': certificates,
    }
    
    return render(request, 'student/certificates.html', context)


@login_required
def achievements_view(request):
    """Student's achievements page."""
    from apps.gamification.models import UserBadge, Achievement
    
    badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    achievements = Achievement.objects.filter(user=request.user)[:20]
    
    context = {
        'badges': badges,
        'achievements': achievements,
    }
    
    return render(request, 'student/achievements.html', context)
