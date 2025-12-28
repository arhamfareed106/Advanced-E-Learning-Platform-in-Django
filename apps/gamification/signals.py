"""
Signals for the gamification system.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import date
from django.db.models import Sum as models_Sum
from apps.enrollment.models import LessonProgress, Enrollment
from apps.quizzes.models import Attempt
from apps.reviews.models import Review
from apps.certificates.models import Certificate
from .models import (
    PointsTransaction, 
    LearningStreak, 
    Achievement, 
    UserBadge,
    Badge
)


@receiver(post_save, sender=LessonProgress)
def update_points_for_lesson_completion(sender, instance, created, **kwargs):
    """
    Award points when a lesson is completed.
    """
    if instance.is_completed and instance.completed_at:
        # Check if points transaction already exists
        if not PointsTransaction.objects.filter(
            user=instance.enrollment.student,
            lesson=instance.lesson,
            transaction_type='lesson_completion'
        ).exists():
            # Award points for lesson completion
            PointsTransaction.objects.create(
                user=instance.enrollment.student,
                transaction_type='lesson_completion',
                points=10,  # 10 points per lesson
                description=f"Completed lesson: {instance.lesson.title}",
                lesson=instance.lesson
            )
            
            # Update streak
            update_learning_streak(instance.enrollment.student)


@receiver(post_save, sender=Enrollment)
def award_points_for_course_enrollment(sender, instance, created, **kwargs):
    """
    Award points when a user enrolls in a course.
    """
    if created:  # Only on creation, not updates
        # Check if points transaction already exists
        if not PointsTransaction.objects.filter(
            user=instance.student,
            course=instance.course,
            transaction_type='enrollment'
        ).exists():
            PointsTransaction.objects.create(
                user=instance.student,
                transaction_type='enrollment',
                points=5,  # 5 points per enrollment
                description=f"Enrolled in course: {instance.course.title}",
                course=instance.course
            )


@receiver(post_save, sender=Attempt)
def award_points_for_quiz_completion(sender, instance, created, **kwargs):
    """
    Award points when a quiz is completed.
    """
    if instance.submitted_at:  # When quiz is submitted
        # Check if points transaction already exists
        if not PointsTransaction.objects.filter(
            user=instance.student,
            quiz=instance.quiz,
            transaction_type='quiz_completion'
        ).exists():
            points = 5 if instance.passed else 2  # More points for passing
            PointsTransaction.objects.create(
                user=instance.student,
                transaction_type='quiz_completion',
                points=points,
                description=f"Completed quiz: {instance.quiz.title} ({'Passed' if instance.passed else 'Failed'})",
                quiz=instance.quiz
            )


@receiver(post_save, sender=Review)
def award_points_for_review_submission(sender, instance, created, **kwargs):
    """
    Award points when a user submits a review.
    """
    if created:  # Only on creation
        # Check if points transaction already exists
        if not PointsTransaction.objects.filter(
            user=instance.student,
            transaction_type='review_submission'
        ).exists():
            PointsTransaction.objects.create(
                user=instance.student,
                transaction_type='review_submission',
                points=15,  # 15 points for review
                description=f"Submitted review for course: {instance.course.title}"
            )


@receiver(post_save, sender=Certificate)
def award_points_for_course_completion(sender, instance, created, **kwargs):
    """
    Award points when a user completes a course and gets a certificate.
    """
    if created:  # Only on creation
        # Check if points transaction already exists
        if not PointsTransaction.objects.filter(
            user=instance.student,
            course=instance.course,
            transaction_type='course_completion'
        ).exists():
            # Award 100 points per completed course
            PointsTransaction.objects.create(
                user=instance.student,
                transaction_type='course_completion',
                points=100,
                description=f"Completed course: {instance.course_name}",
                course=instance.course
            )
            
            # Create course completion achievement
            Achievement.objects.create(
                user=instance.student,
                title=f"Completed {instance.course_name}",
                description=f"Successfully completed the course {instance.course_name}",
                icon="fas fa-graduation-cap",
                points=100,
                achievement_type='course_completion',
                course=instance.course
            )


def update_learning_streak(user):
    """
    Update the user's learning streak.
    """
    today = date.today()
    
    # Get or create the user's streak record
    streak, created = LearningStreak.objects.get_or_create(user=user)
    
    # If this is the first activity or yesterday's activity
    if streak.last_activity_date is None or streak.last_activity_date == today:
        # Either first activity or same day activity - no change to streak
        streak.last_activity_date = today
    elif (today - streak.last_activity_date).days == 1:
        # Consecutive day - increment streak
        streak.current_streak += 1
        streak.last_activity_date = today
        # Update longest streak if needed
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
    else:
        # Not consecutive - reset streak
        streak.current_streak = 1
        streak.last_activity_date = today
    
    streak.save()
    
    # Award streak bonus if applicable
    if streak.current_streak > 1 and streak.current_streak % 5 == 0:  # Every 5 days
        # Check if streak bonus was already awarded for this streak length
        if not PointsTransaction.objects.filter(
            user=user,
            transaction_type='streak_bonus',
            description=f"Learning streak of {streak.current_streak} days"
        ).exists():
            bonus_points = streak.current_streak * 2  # 2 points per day in streak
            PointsTransaction.objects.create(
                user=user,
                transaction_type='streak_bonus',
                points=bonus_points,
                description=f"Learning streak of {streak.current_streak} days"
            )
            
            # Create streak achievement
            Achievement.objects.create(
                user=user,
                title=f"{streak.current_streak} Day Streak!",
                description=f"Achieved a learning streak of {streak.current_streak} days",
                icon="fas fa-fire",
                points=bonus_points,
                achievement_type='streak'
            )


@receiver(post_save, sender=PointsTransaction)
def update_user_badges(sender, instance, created, **kwargs):
    """
    Check if user has earned any new badges based on points.
    """
    if created:
        # Get all badges that the user doesn't already have
        user_badges = instance.user.user_badges.values_list('badge_id', flat=True)
        available_badges = Badge.objects.exclude(id__in=user_badges)
        
        for badge in available_badges:
            # Check if user has enough points for this badge
            total_points = instance.user.points_transactions.aggregate(
                total=models_Sum('points')
            )['total'] or 0
            
            if total_points >= badge.points_required:
                # Award the badge
                UserBadge.objects.create(user=instance.user, badge=badge)
                
                # Create achievement for earning badge
                Achievement.objects.create(
                    user=instance.user,
                    title=f"Earned {badge.name}",
                    description=badge.description,
                    icon=badge.icon,
                    points=badge.points_required,
                    achievement_type='achievement',
                )