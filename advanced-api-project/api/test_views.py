"""
Unit tests for the Book API endpoints.

Testing strategy:
- CRUD operations: Create, Retrieve, Update, Delete with correct status codes and data
- Filtering: title, author, author__name, publication_year
- Search: search parameter across title and author name
- Ordering: ordering by title, publication_year, author__name
- Permissions: AllowAny for list/detail, IsAuthenticated for create/update/delete
- Validation: publication_year not in future

Run tests: python manage.py test api.test_views
"""
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Author, Book

User = get_user_model()


class BookAPITestCase(APITestCase):
    """Base test case with fixtures for books and authors."""

    def setUp(self):
        """Create test data: authors, books, and an authenticated user."""
        self.author1 = Author.objects.create(name='Jane Austen')
        self.author2 = Author.objects.create(name='Charles Dickens')

        self.book1 = Book.objects.create(
            title='Pride and Prejudice',
            publication_year=date(1813, 1, 28),
            author=self.author1,
        )
        self.book2 = Book.objects.create(
            title='Sense and Sensibility',
            publication_year=date(1811, 1, 1),
            author=self.author1,
        )
        self.book3 = Book.objects.create(
            title='Great Expectations',
            publication_year=date(1861, 1, 1),
            author=self.author2,
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )


# ------------------------------------------------------------------------------
# CRUD Operation Tests
# ------------------------------------------------------------------------------

class BookListTests(BookAPITestCase):
    """Tests for GET /books/ (list)."""

    def test_list_books_returns_200(self):
        """List endpoint returns 200 OK."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_books_returns_all_books(self):
        """List returns all books with correct structure."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)
        self.assertIn('id', response.data[0])
        self.assertIn('title', response.data[0])
        self.assertIn('publication_year', response.data[0])
        self.assertIn('author', response.data[0])

    def test_list_books_author_nested(self):
        """Each book includes nested author object."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        first_book = response.data[0]
        self.assertIn('author', first_book)
        self.assertIn('name', first_book['author'])


class BookDetailTests(BookAPITestCase):
    """Tests for GET /books/<pk>/ (detail)."""

    def test_detail_returns_200(self):
        """Detail endpoint returns 200 for valid pk."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_returns_correct_data(self):
        """Detail returns correct book data."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.data['title'], 'Pride and Prejudice')
        self.assertEqual(response.data['author']['name'], 'Jane Austen')

    def test_detail_404_for_invalid_pk(self):
        """Detail returns 404 for non-existent book."""
        url = reverse('api:book-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateTests(BookAPITestCase):
    """Tests for POST /books/create/ (create)."""

    def test_create_requires_authentication(self):
        """Create without auth returns 403."""
        url = reverse('api:book-create')
        data = {
            'title': 'New Book',
            'publication_year': '2020-01-01',
            'author': self.author1.pk,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_with_auth_returns_201(self):
        """Create with auth returns 201 and saves book."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('api:book-create')
        data = {
            'title': 'New Book',
            'publication_year': '2020-01-01',
            'author': self.author1.pk,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(Book.objects.count(), 4)

    def test_create_validates_future_publication_year(self):
        """Create rejects publication_year in the future."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('api:book-create')
        data = {
            'title': 'Future Book',
            'publication_year': '2030-01-01',
            'author': self.author1.pk,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)


class BookUpdateTests(BookAPITestCase):
    """Tests for GET/PUT/PATCH /books/<pk>/update/ (update)."""

    def test_update_requires_authentication(self):
        """Update without auth returns 403."""
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_with_auth_returns_200(self):
        """Update with auth returns 200 and saves changes."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_update_rejects_future_publication_year(self):
        """Update rejects publication_year in the future."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {'publication_year': '2030-01-01'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)


class BookDeleteTests(BookAPITestCase):
    """Tests for DELETE /books/<pk>/delete/ (delete)."""

    def test_delete_requires_authentication(self):
        """Delete without auth returns 403."""
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_with_auth_removes_book(self):
        """Delete with auth returns 204 and removes book."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('api:book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())


# ------------------------------------------------------------------------------
# Filtering Tests
# ------------------------------------------------------------------------------

class BookFilterTests(BookAPITestCase):
    """Tests for filtering on list endpoint."""

    def test_filter_by_title(self):
        """?title=Pride returns matching books."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'title': 'Pride'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')

    def test_filter_by_author(self):
        """?author=<id> returns books by that author."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': self.author1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_author_name(self):
        """?author__name=Austen returns books by authors with that name."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author__name': 'Austen'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_publication_year(self):
        """?publication_year= returns books with exact date."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': '1813-01-28'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')

    def test_filter_publication_year_after(self):
        """?publication_year_after= returns books published on or after date."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year_after': '1812-01-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Pride (1813), Sense (1811)? No - 1811 is before 1812
        # 1813, 1861 are after 1812. 1811 is before. So 2 books.
        titles = [b['title'] for b in response.data]
        self.assertIn('Pride and Prejudice', titles)
        self.assertIn('Great Expectations', titles)


# ------------------------------------------------------------------------------
# Search Tests
# ------------------------------------------------------------------------------

class BookSearchTests(BookAPITestCase):
    """Tests for search on list endpoint."""

    def test_search_matches_title(self):
        """?search=Pride returns books with 'Pride' in title."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Pride'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')

    def test_search_matches_author_name(self):
        """?search=Austen returns books by authors with 'Austen' in name."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Austen'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


# ------------------------------------------------------------------------------
# Ordering Tests
# ------------------------------------------------------------------------------

class BookOrderingTests(BookAPITestCase):
    """Tests for ordering on list endpoint."""

    def test_ordering_by_title_asc(self):
        """?ordering=title returns books sorted by title A-Z."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b['title'] for b in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_title_desc(self):
        """?ordering=-title returns books sorted by title Z-A."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b['title'] for b in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_ordering_by_publication_year_desc(self):
        """?ordering=-publication_year returns newest first."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Great Expectations')


# ------------------------------------------------------------------------------
# Permission Tests
# ------------------------------------------------------------------------------

class BookPermissionTests(BookAPITestCase):
    """Tests for permission enforcement."""

    def test_list_allowed_without_auth(self):
        """List and detail are accessible without authentication."""
        self.client.logout()
        list_resp = self.client.get(reverse('api:book-list'))
        detail_resp = self.client.get(
            reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        )
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_resp.status_code, status.HTTP_200_OK)

    def test_create_update_delete_require_auth(self):
        """Create, update, delete require authentication."""
        self.client.logout()
        create_resp = self.client.post(
            reverse('api:book-create'),
            {'title': 'X', 'publication_year': '2020-01-01', 'author': self.author1.pk},
            format='json',
        )
        update_resp = self.client.patch(
            reverse('api:book-update', kwargs={'pk': self.book1.pk}),
            {'title': 'Y'},
            format='json',
        )
        delete_resp = self.client.delete(
            reverse('api:book-delete', kwargs={'pk': self.book1.pk}),
        )
        self.assertEqual(create_resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(update_resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_resp.status_code, status.HTTP_403_FORBIDDEN)
