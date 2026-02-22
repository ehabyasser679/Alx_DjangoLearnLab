from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications'
    )
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications'
    )
    verb = models.CharField(max_length=255)  # e.g. "liked your post", "followed you", "commented on"

    # Generic relation so a notification can point at any object (Post, Comment …)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'target_object_id')

    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor.username} {self.verb} → {self.recipient.username}"
