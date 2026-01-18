from typing import Optional
from django.db.models import QuerySet

from relationship_app.models import Book, Library, Librarian


def query_books_by_author(author_name: str) -> QuerySet:
    return Book.objects.filter(author__name=author_name)


def list_books_in_library(library_name: str) -> QuerySet:
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return Book.objects.none()
    return library.books.all()


def get_librarian_for_library(library_name: str) -> Optional[Librarian]:
    try:
        return Librarian.objects.get(library__name=library_name)
    except Librarian.DoesNotExist:
        return None





