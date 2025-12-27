"""
Views for notifications app.
"""

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """List all notifications for the current user."""
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            is_read_bool = is_read.lower() == 'true'
            queryset = queryset.filter(is_read=is_read_bool)
        
        return queryset.order_by('-created_at')


class NotificationMarkReadView(views.APIView):
    """Mark notification as read."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        notification = get_object_or_404(
            Notification,
            id=pk,
            user=request.user
        )
        notification.mark_as_read()
        return Response(NotificationSerializer(notification).data)


class NotificationMarkAllReadView(views.APIView):
    """Mark all notifications as read."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )
        
        from django.utils import timezone
        now = timezone.now()
        
        for notification in notifications:
            notification.is_read = True
            notification.read_at = now
        
        Notification.objects.bulk_update(notifications, ['is_read', 'read_at'])
        
        return Response({
            'message': f'{notifications.count()} notifications marked as read.'
        })


class NotificationUnreadCountView(views.APIView):
    """Get unread notification count."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        return Response({'count': count})
