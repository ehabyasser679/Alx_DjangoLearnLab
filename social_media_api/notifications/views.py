from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    GET /api/notifications/
    Returns all notifications for the authenticated user, newest first.
    Unread notifications appear with is_read=false.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('actor', 'recipient')


class MarkNotificationReadView(APIView):
    """
    POST /api/notifications/<id>/read/
    Marks a specific notification as read.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response(
                {'detail': 'Notification not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({'detail': 'Marked as read.'}, status=status.HTTP_200_OK)


class MarkAllReadView(APIView):
    """
    POST /api/notifications/read-all/
    Marks all of the authenticated user's notifications as read.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).update(is_read=True)
        return Response(
            {'detail': f'{updated} notification(s) marked as read.'},
            status=status.HTTP_200_OK,
        )
