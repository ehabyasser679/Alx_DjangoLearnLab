"""
Book API Filters

Provides filtering, searching, and ordering capabilities for the Book list view.
- BookFilter: DjangoFilterBackend filter set for title, author, publication_year
- SearchFilter: Text search on title and author name
- OrderingFilter: Sort by title, publication_year, author
"""
import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    """
    FilterSet for Book model.

    Filter options:
    - title: Case-insensitive partial match (icontains)
    - author: Filter by author ID (exact)
    - author__name: Filter by author name (case-insensitive partial)
    - publication_year: Filter by exact date
    - publication_year_after: Books published on or after this date
    - publication_year_before: Books published on or before this date
    """

    title = django_filters.CharFilter(lookup_expr='icontains', label='Title (partial match)')
    author = django_filters.NumberFilter(field_name='author', label='Author ID')
    author__name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        label='Author name (partial match)',
    )
    publication_year = django_filters.DateFilter(field_name='publication_year', label='Publication date (exact)')
    publication_year_after = django_filters.DateFilter(
        field_name='publication_year',
        lookup_expr='gte',
        label='Published on or after',
    )
    publication_year_before = django_filters.DateFilter(
        field_name='publication_year',
        lookup_expr='lte',
        label='Published on or before',
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
