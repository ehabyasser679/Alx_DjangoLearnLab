from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    list_filter = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'created_at']
    search_fields = ['content', 'author__username']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
