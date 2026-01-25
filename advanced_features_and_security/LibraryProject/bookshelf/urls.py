from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="bookshelf-index"),
    path("create/", views.create_book, name="bookshelf-create"),
    path("<int:pk>/", views.book_detail, name="bookshelf-detail"),
    path("<int:pk>/edit/", views.edit_book, name="bookshelf-edit"),
    path("<int:pk>/delete/", views.delete_book, name="bookshelf-delete"),
]