from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    TokenRetrieveView,
    ProfileView,
    FollowView,
    UnfollowView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenRetrieveView.as_view(), name='token-retrieve'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowView.as_view(), name='unfollow'),
]
