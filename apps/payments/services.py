"""
Stripe payment service.
"""

import stripe
from django.conf import settings
from .models import PaymentTransaction

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(user, course, success_url, cancel_url):
    """
    Create a Stripe checkout session for course purchase.
    
    Args:
        user: User making the purchase
        course: Course to purchase
        success_url: URL to redirect on success
        cancel_url: URL to redirect on cancel
    
    Returns:
        dict: Session data with session_id and url
    """
    try:
        # Create or get Stripe customer
        if not user.profile.metadata.get('stripe_customer_id'):
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}".strip() or user.username,
                metadata={'user_id': str(user.id)}
            )
            customer_id = customer.id
            
            # Save customer ID to user profile
            user.profile.metadata['stripe_customer_id'] = customer_id
            user.profile.save()
        else:
            customer_id = user.profile.metadata['stripe_customer_id']
        
        # Create checkout session
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(course.price * 100),  # Convert to cents
                    'product_data': {
                        'name': course.title,
                        'description': course.description[:500],
                        'images': [course.thumbnail.url] if course.thumbnail else [],
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'user_id': str(user.id),
                'course_id': str(course.id),
            }
        )
        
        # Create payment transaction record
        PaymentTransaction.objects.create(
            user=user,
            course=course,
            payment_type='course',
            amount=course.price,
            currency='USD',
            status='pending',
            stripe_session_id=session.id,
            stripe_customer_id=customer_id,
            description=f"Purchase of {course.title}",
            metadata={
                'course_id': str(course.id),
                'course_title': course.title,
            }
        )
        
        return {
            'session_id': session.id,
            'url': session.url
        }
    
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


def handle_successful_payment(session_id):
    """
    Handle successful payment from Stripe webhook.
    
    Args:
        session_id: Stripe session ID
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Get payment transaction
        transaction = PaymentTransaction.objects.filter(
            stripe_session_id=session_id
        ).first()
        
        if transaction and transaction.status == 'pending':
            from django.utils import timezone
            
            transaction.status = 'completed'
            transaction.stripe_payment_intent_id = session.payment_intent
            transaction.completed_at = timezone.now()
            transaction.save()
            
            # Auto-enroll user in course
            if transaction.course:
                from apps.enrollment.models import Enrollment
                Enrollment.objects.get_or_create(
                    student=transaction.user,
                    course=transaction.course
                )
    
    except Exception as e:
        print(f"Error handling successful payment: {str(e)}")
