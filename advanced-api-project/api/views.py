"""
Book API Views

These views provide CRUD operations for Book instances. Permissions are configured
so that read operations (list, detail) are public, while write operations
(create, update, delete) require authentication.

Filtering, Search, and Ordering (ListView):
- DjangoFilterBackend: Filter by title, author, author__name, publication_year
- SearchFilter: Text search across title and author name (?search=...)
- OrderingFilter: Sort by title, publication_year, author (?ordering=...)
"""
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework

from .filters import BookFilter
from .models import Book
from .serializers import BookSerializer


# ------------------------------------------------------------------------------
# Read-only views (public access)
# ------------------------------------------------------------------------------

class ListView(generics.ListAPIView):
    """
    GET /books/
    List all books with filtering, search, and ordering.

    Filtering (DjangoFilterBackend):
    - ?title=<partial> - Title contains (case-insensitive)
    - ?author=<id> - Author ID (exact)
    - ?author__name=<partial> - Author name contains (case-insensitive)
    - ?publication_year=<YYYY-MM-DD> - Exact publication date
    - ?publication_year_after=<YYYY-MM-DD> - Published on or after
    - ?publication_year_before=<YYYY-MM-DD> - Published on or before

    Search (SearchFilter):
    - ?search=<query> - Searches title and author name

    Ordering (OrderingFilter):
    - ?ordering=title - Sort by title (asc)
    - ?ordering=-title - Sort by title (desc)
    - ?ordering=publication_year - Sort by date (asc)
    - ?ordering=-publication_year - Sort by date (desc)
    - ?ordering=author - Sort by author name (asc)
    - ?ordering=-author - Sort by author name (desc)
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    queryset = Book.objects.all().select_related('author')

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering


class DetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/
    Retrieve a single book by primary key.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


# ------------------------------------------------------------------------------
# Write views (authenticated users only)
# ------------------------------------------------------------------------------

class CreateView(generics.CreateAPIView):
    """
    POST /books/create/
    Create a new book. Requires authentication.

    Request body (JSON): {"title": "...", "publication_year": "YYYY-MM-DD", "author": <author_id>}
    Data validation is performed by BookSerializer (e.g., publication_year not in future).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the book. Override for logging, notifications, etc."""
        serializer.save()


class UpdateView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /books/<pk>/update/
    Retrieve (GET) or update (PUT/PATCH) a book. Requires authentication for writes.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Save the updated book. Override for auditing, etc."""
        serializer.save()


class DeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<pk>/delete/
    Delete a book. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

