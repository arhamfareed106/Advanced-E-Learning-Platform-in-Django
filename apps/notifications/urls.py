"""
URL patterns for notifications API.
"""

from django.urls import path
from .views import (
    NotificationListView, NotificationMarkReadView,
    NotificationMarkAllReadView, NotificationUnreadCountView
)

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('unread-count/', NotificationUnreadCountView.as_view(), name='unread_count'),
    path('<uuid:pk>/mark-read/', NotificationMarkReadView.as_view(), name='mark_read'),
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='mark_all_read'),
]
