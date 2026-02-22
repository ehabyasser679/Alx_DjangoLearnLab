from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
import re

PASSWORD_REGEX = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer used for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_password(self, value):
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                'Password must be at least 8 characters and include an uppercase letter, '
                'a lowercase letter, a digit, and a special character (@$!%*?&).'
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing and updating a user's profile."""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'email', 'bio', 'profile_picture', 'followers_count']

    def get_followers_count(self, obj):
        return obj.followers.count()