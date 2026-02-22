from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Profile
import re

User = get_user_model()

PASSWORD_REGEX = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer used for user registration. Creates the user and their auth token."""
    password = serializers.CharField()
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'token']

    def validate_password(self, value):
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                'Password must be at least 8 characters and include an uppercase letter, '
                'a lowercase letter, a digit, and a special character (@$!%*?&).'
            )
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        Token.objects.create(user=user)
        return user

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing and updating a user's profile."""
    username = serializers.CharField()
    email = serializers.EmailField(source='user.email', read_only=True)
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'email', 'bio', 'profile_picture', 'followers_count']

    def get_followers_count(self, obj):
        return obj.followers.count()
