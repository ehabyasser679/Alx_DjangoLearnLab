"""
Book API Views

These views provide CRUD operations for Book instances. Permissions are configured
so that read operations (list, detail) are public, while write operations
(create, update, delete) require authentication.

Custom hooks:
- perform_create/perform_update: Override points for logging or side effects.
- get_queryset: Supports filtering by title and publication_year via query params.
"""
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


# ------------------------------------------------------------------------------
# Read-only views (public access)
# ------------------------------------------------------------------------------

class ListView(generics.ListAPIView):
    """
    GET /books/
    List all books. Supports optional filtering via query parameters:
    - ?title=<partial> - Filter by title (case-insensitive contains)
    - ?publication_year=<YYYY-MM-DD> - Filter by exact publication date
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Book.objects.all().select_related('author')
        title = self.request.query_params.get('title', None)
        publication_year = self.request.query_params.get('publication_year', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if publication_year:
            queryset = queryset.filter(publication_year=publication_year)
        return queryset


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

