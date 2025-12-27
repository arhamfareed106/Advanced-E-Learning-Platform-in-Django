"""
URL patterns for payments API.
"""

from django.urls import path
from .views import CreateCheckoutSessionView, StripeWebhookView, PaymentHistoryView

app_name = 'payments'

urlpatterns = [
    path('create-checkout/', CreateCheckoutSessionView.as_view(), name='create_checkout'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),
    path('history/', PaymentHistoryView.as_view(), name='payment_history'),
]
