"""
Admin configuration for payments app.
"""

from django.contrib import admin
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'amount', 'currency', 'status', 'payment_type', 'created_at', 'completed_at']
    list_filter = ['status', 'payment_type', 'created_at']
    search_fields = ['user__username', 'course__title', 'stripe_payment_intent_id']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
