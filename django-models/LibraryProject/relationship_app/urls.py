"""
URL configuration for relationship_app.
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from relationship_app import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('libraries/', views.LibrarylistView.as_view(), name='library-list'),
    path('libraries/<int:pk>/', views.LibrarydetailView.as_view(), name='library-detail'),
    path('books/', views.all_books_view, name='book-list'),
    path('add_book/', views.add_book, name='book-add'),
    path('edit_book/<int:pk>/', views.edit_book, name='book-edit'),
    path('books/<int:pk>/delete/', views.delete_book, name='book-delete'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name="relationship_app/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="relationship_app/logout.html"), name='logout'),
    path('admin/', views.admin_view, name='admin-view'),
    path('librarian/', views.librarian_view, name='librarian-view'),
    path('member/', views.member_view, name='member-view'),
]

