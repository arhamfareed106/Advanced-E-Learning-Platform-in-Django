"""
Template views for student dashboard.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db import OperationalError
from apps.enrollment.models import Enrollment, LessonProgress
from apps.certificates.models import Certificate
from apps.courses.models import Course


@login_required
def dashboard_view(request):
    """Student dashboard page."""
    # Get student's enrollments
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')[:5]
    
    # Get certificates
    certificates = Certificate.objects.filter(student=request.user)[:3]
    
    # Get badges (handle missing table)
    try:
        from apps.gamification.models import UserBadge, Leaderboard, LearningStreak
        badges = UserBadge.objects.filter(user=request.user).select_related('badge')[:6]
        
        # Get leaderboard entry
        try:
            leaderboard = Leaderboard.objects.get(user=request.user)
            level = leaderboard.level
            points = leaderboard.points
            rank = leaderboard.rank
        except (Leaderboard.DoesNotExist, OperationalError):
            level = 1
            points = 0
            rank = 0
        
        # Get learning streak
        try:
            streak = LearningStreak.objects.get(user=request.user)
            streak_count = streak.current_streak
        except (LearningStreak.DoesNotExist, OperationalError):
            streak_count = 0
        
        # Get total points from transactions
        try:
            from apps.gamification.models import PointsTransaction
            total_points = PointsTransaction.objects.filter(
                user=request.user
            ).aggregate(total=Sum('points'))['total'] or 0
        except OperationalError:
            total_points = 0
    except (ImportError, OperationalError):
        badges = []
        level = 1
        points = 0
        rank = 0
        streak_count = 0
        total_points = 0
    
    # Calculate learning hours
    try:
        total_seconds = LessonProgress.objects.filter(
            enrollment__student=request.user
        ).aggregate(total=Sum('watch_time_seconds'))['total'] or 0
        learning_hours = int(total_seconds / 3600)
    except OperationalError:
        learning_hours = 0
    
    context = {
        'recent_enrollments': enrollments,
        'certificates_count': certificates.count(),
        'enrollments_count': enrollments.count(),
        'badges_count': len(badges) if isinstance(badges, list) else badges.count(),
        'recent_badges': badges,
        'level': level,
        'points': points,
        'total_points': total_points,
        'rank': rank,
        'next_level_points': level * 100,
        'progress_percentage': min((points % 100), 100),
        'streak': streak_count,
        'learning_hours': learning_hours,
        'current_streak': streak_count,
    }
    
    return render(request, 'student/dashboard.html', context)


@login_required
def my_courses_view(request):
    """Student's enrolled courses page."""
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    # Calculate stats
    completed_count = enrollments.filter(is_completed=True).count()
    in_progress_count = enrollments.filter(is_completed=False).count()
    
    context = {
        'enrollments': enrollments,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
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
    # Get badges (handle missing table)
    try:
        from apps.gamification.models import UserBadge, Leaderboard, LearningStreak
        badges = UserBadge.objects.filter(user=request.user).select_related('badge')
        
        # Get leaderboard entry
        try:
            leaderboard = Leaderboard.objects.get(user=request.user)
            level = leaderboard.level
            total_points = leaderboard.points
        except (Leaderboard.DoesNotExist, OperationalError):
            level = 1
            total_points = 0
        
        # Get learning streak
        try:
            streak = LearningStreak.objects.get(user=request.user)
            current_streak = streak.current_streak
        except (LearningStreak.DoesNotExist, OperationalError):
            current_streak = 0
    except (ImportError, OperationalError):
        badges = []
        level = 1
        total_points = 0
        current_streak = 0
    
    context = {
        'badges': badges,
        'level': level,
        'total_points': total_points,
        'current_streak': current_streak,
    }
    
    return render(request, 'student/achievements.html', context)
