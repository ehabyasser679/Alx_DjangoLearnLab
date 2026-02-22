from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    recipient_username = serializers.ReadOnlyField(source='recipient.username')
    target_str = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_username',
            'actor', 'actor_username',
            'verb', 'target_str',
            'is_read', 'timestamp',
        ]
        read_only_fields = [
            'recipient', 'actor', 'verb',
            'target_str', 'timestamp',
        ]

    def get_target_str(self, obj):
        """Human-readable representation of the target object."""
        if obj.target:
            return str(obj.target)
        return None
