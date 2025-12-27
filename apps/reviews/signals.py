"""
Signals for automatic review aggregation.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_course_rating(sender, instance, **kwargs):
    """
    Update course average rating and review count when a review is added/updated/deleted.
    """
    course = instance.course
    
    # Calculate average rating
    avg_rating = course.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    review_count = course.reviews.count()
    
    course.average_rating = round(avg_rating, 2)
    course.review_count = review_count
    course.save(update_fields=['average_rating', 'review_count'])
