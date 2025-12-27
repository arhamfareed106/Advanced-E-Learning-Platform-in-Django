"""
Views for payments app.
"""

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import stripe

from .models import PaymentTransaction
from apps.courses.models import Course
from .serializers import PaymentTransactionSerializer
from .services import create_checkout_session, handle_successful_payment


class CreateCheckoutSessionView(views.APIView):
    """Create Stripe checkout session for course purchase."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        course_id = request.data.get('course_id')
        
        if not course_id:
            return Response({
                'error': 'course_id is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        course = get_object_or_404(Course, id=course_id, status='published')
        
        if course.is_free:
            return Response({
                'error': 'This course is free.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already purchased
        existing_payment = PaymentTransaction.objects.filter(
            user=request.user,
            course=course,
            status='completed'
        ).exists()
        
        if existing_payment:
            return Response({
                'error': 'You have already purchased this course.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            success_url = f"{settings.FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}"
            cancel_url = f"{settings.FRONTEND_URL}/courses/{course.slug}"
            
            session_data = create_checkout_session(
                user=request.user,
                course=course,
                success_url=success_url,
                cancel_url=cancel_url
            )
            
            return Response(session_data)
        
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(views.APIView):
    """Handle Stripe webhooks."""
    
    permission_classes = []
    
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            handle_successful_payment(session['id'])
        
        return Response({'status': 'success'})


class PaymentHistoryView(generics.ListAPIView):
    """List payment history for the current user."""
    
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user).order_by('-created_at')
