from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikeView, FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'posts/(?P<post_pk>[^/.]+)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pk>/like/', LikeView.as_view(), name='post-like'),
    path('posts/feed/', FeedView.as_view(), name='post-feed'),
]
