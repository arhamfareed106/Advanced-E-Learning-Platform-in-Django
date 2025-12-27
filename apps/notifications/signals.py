"""
Signals for automatic notification creation.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.enrollment.models import Enrollment
from apps.quizzes.models import Quiz
from apps.certificates.models import Certificate
from apps.payments.models import PaymentTransaction
from .models import Notification


@receiver(post_save, sender=Enrollment)
def create_enrollment_notification(sender, instance, created, **kwargs):
    """Create notification when student enrolls in a course."""
    if created:
        Notification.objects.create(
            user=instance.student,
            notification_type='enrollment',
            title='Successfully Enrolled!',
            message=f'You have successfully enrolled in "{instance.course.title}".',
            action_url=f'/student/courses/{instance.course.id}/',
            metadata={'course_id': str(instance.course.id)}
        )


@receiver(post_save, sender=Quiz)
def create_quiz_added_notification(sender, instance, created, **kwargs):
    """Notify enrolled students when a new quiz is added."""
    if created:
        # Get all enrolled students
        enrollments = instance.course.enrollments.all()
        notifications = [
            Notification(
                user=enrollment.student,
                notification_type='quiz_added',
                title='New Quiz Available!',
                message=f'A new quiz "{instance.title}" has been added to "{instance.course.title}".',
                action_url=f'/student/courses/{instance.course.id}/quizzes/{instance.id}/',
                metadata={'course_id': str(instance.course.id), 'quiz_id': str(instance.id)}
            )
            for enrollment in enrollments
        ]
        Notification.objects.bulk_create(notifications)


@receiver(post_save, sender=Certificate)
def create_certificate_notification(sender, instance, created, **kwargs):
    """Create notification when certificate is generated."""
    if created:
        Notification.objects.create(
            user=instance.student,
            notification_type='certificate',
            title='Certificate Earned! 🎉',
            message=f'Congratulations! You have earned a certificate for completing "{instance.course_name}".',
            action_url=f'/certificates/{instance.id}/',
            metadata={'certificate_id': str(instance.id)}
        )


@receiver(post_save, sender=PaymentTransaction)
def create_payment_notification(sender, instance, **kwargs):
    """Create notification for payment status changes."""
    if instance.status == 'completed' and not instance.user.notifications.filter(
        notification_type='payment',
        metadata__payment_id=str(instance.id)
    ).exists():
        Notification.objects.create(
            user=instance.user,
            notification_type='payment',
            title='Payment Successful!',
            message=f'Your payment of {instance.amount} {instance.currency} has been processed successfully.',
            action_url='/student/dashboard/',
            metadata={'payment_id': str(instance.id)}
        )
