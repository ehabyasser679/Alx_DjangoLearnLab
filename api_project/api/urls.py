from django.contrib import admin
from django.urls import path, include
from api import views
from .views import BookListCreateAPIView, BookList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename = 'book_all')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/books", views.BookListCreateAPIView.as_view(), name="book_list_create"),
    path('api/', include('api.urls')),
    path('', BookList.as_view(), name='book_list'),
    path('api/', include(router.urls)),
]
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename = 'book_all')

