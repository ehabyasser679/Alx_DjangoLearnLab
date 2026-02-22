from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipient', 'actor', 'verb', 'is_read', 'timestamp']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['actor__username', 'recipient__username', 'verb']
