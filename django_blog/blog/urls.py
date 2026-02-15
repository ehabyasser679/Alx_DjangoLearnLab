from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path("profile/", views.profile, name= "profile"),
    path("post/", BlogListView.as_view(), name= "posts"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name= "post_detail"),
    path("post/new/", BlogCreateView.as_view(), name= "post_new"),
    path("post/<int:pk>/update/", BlogUpdateView.as_view(), name= "post_edit"),
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name= "post_delete"),
]


