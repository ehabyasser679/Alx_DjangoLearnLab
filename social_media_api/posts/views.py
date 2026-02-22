from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification


# ──────────────────────────────────────────────────────────
# Pagination
# ──────────────────────────────────────────────────────────

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ──────────────────────────────────────────────────────────
# Post ViewSet  (list / create / retrieve / update / destroy)
# ──────────────────────────────────────────────────────────

class PostViewSet(viewsets.ModelViewSet):
    """
    GET    /api/posts/           – paginated list; searchable by title & content
    POST   /api/posts/           – create (authenticated)
    GET    /api/posts/<id>/      – detail
    PUT    /api/posts/<id>/      – update (author only)
    PATCH  /api/posts/<id>/      – partial update (author only)
    DELETE /api/posts/<id>/      – delete (author only)
    """
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ──────────────────────────────────────────────────────────
# Comment ViewSet  (nested under posts)
# ──────────────────────────────────────────────────────────

class CommentViewSet(viewsets.ModelViewSet):
    """
    GET    /api/posts/<post_pk>/comments/        – list comments for a post
    POST   /api/posts/<post_pk>/comments/        – create comment (authenticated)
    GET    /api/posts/<post_pk>/comments/<id>/   – comment detail
    PUT    /api/posts/<post_pk>/comments/<id>/   – update (author only)
    DELETE /api/posts/<post_pk>/comments/<id>/   – delete (author only)
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_pk).select_related('author')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        comment = serializer.save(author=self.request.user, post=post)

        # Notify the post author (unless they commented on their own post)
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb='commented on your post',
                content_type=ContentType.objects.get_for_model(comment),
                target_object_id=comment.pk,
            )


# ──────────────────────────────────────────────────────────
# Like / Unlike  (single resource, not a viewset)
# ──────────────────────────────────────────────────────────

class LikeView(APIView):
    """
    POST   /api/posts/<pk>/like/    – like a post
    DELETE /api/posts/<pk>/like/    – unlike a post
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response(
                {'detail': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Notify the post author (not if they liked their own post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.pk,
            )

        return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if not deleted:
            return Response(
                {'detail': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'detail': 'Post unliked.'}, status=status.HTTP_204_NO_CONTENT)


# ──────────────────────────────────────────────────────────
# Feed — posts from followed users
# ──────────────────────────────────────────────────────────

class FeedView(generics.ListAPIView):
    """
    GET /api/posts/feed/
    Returns posts from all users that the current user follows,
    ordered newest-first, paginated.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        # Profile.followers is a M2M of User objects that follow *this* user.
        # We want posts where the author is followed *by* the current user.
        # The Profile.followers field stores: users that follow the profile owner.
        # So "users I follow" = User objects whose profile lists me in .followers
        following_users = User.objects.filter(
            profile__followers=self.request.user
        )
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
