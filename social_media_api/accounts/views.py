from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserProfileSerializer
from notifications.models import Notification


class RegisterView(APIView):
    """
    POST /api/accounts/register/
    Body: { "username": "...", "password": "...", "email": "..." }
    Returns a token on success.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user_id': user.pk,
                    'username': user.username,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/accounts/login/
    Body: { "username": "...", "password": "..." }
    Returns a token on success.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'user_id': user.pk, 'username': user.username},
            status=status.HTTP_200_OK,
        )


class TokenRetrieveView(APIView):
    """
    GET /api/accounts/token/
    Requires: Authorization: Token <token>
    Returns the current user's token.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token, _ = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    GET  /api/accounts/profile/  – retrieve the authenticated user's profile.
    PUT  /api/accounts/profile/  – update bio / profile_picture.
    Requires: Authorization: Token <token>
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user.profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowView(APIView):
    """
    POST /api/accounts/follow/<user_id>/
    Follows the target user and creates a 'followed you' notification.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)

        if target_user == request.user:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Profile.followers stores which users follow the profile owner.
        # So to follow target_user, we add request.user to target_user.profile.followers
        profile = target_user.profile
        if request.user in profile.followers.all():
            return Response(
                {'detail': f'You are already following {target_user.username}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile.followers.add(request.user)

        # Notify the followed user
        Notification.objects.create(
            recipient=target_user,
            actor=request.user,
            verb='followed you',
        )

        return Response(
            {'detail': f'You are now following {target_user.username}.'},
            status=status.HTTP_200_OK,
        )


class UnfollowView(APIView):
    """
    POST /api/accounts/unfollow/<user_id>/
    Unfollows the target user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)

        if target_user == request.user:
            return Response(
                {'detail': 'You cannot unfollow yourself.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = target_user.profile
        if request.user not in profile.followers.all():
            return Response(
                {'detail': f'You are not following {target_user.username}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile.followers.remove(request.user)
        return Response(
            {'detail': f'You have unfollowed {target_user.username}.'},
            status=status.HTTP_200_OK,
        )