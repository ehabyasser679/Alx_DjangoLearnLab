# Advanced API Project

Django REST Framework API for managing Books and Authors with permission-based access control.

## Setup

```bash
# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (for admin and API auth)
python manage.py createsuperuser
```

## Filtering, Search & Ordering Implementation

The Book list endpoint uses three DRF filter backends:

1. **DjangoFilterBackend** — Uses `BookFilter` in `api/filters.py` for attribute-based filtering.
2. **SearchFilter** — Searches across `title` and `author__name` fields.
3. **OrderingFilter** — Allows sorting by `title`, `publication_year`, or `author__name`.

Filter, search, and ordering parameters can be combined in a single request.

## API Overview

| Endpoint | Method | Auth required | Description |
|----------|--------|---------------|-------------|
| `/books/` | GET | No | List all books (supports filters) |
| `/books/create/` | POST | Yes | Create a new book |
| `/books/<id>/` | GET | No | Get a single book |
| `/books/<id>/update/` | GET, PUT, PATCH | Yes | Retrieve or update a book |
| `/books/<id>/delete/` | DELETE | Yes | Delete a book |

### Permissions

- **Read-only (public)**: `ListView` and `DetailView` use `AllowAny` — no authentication needed.
- **Write (authenticated)**: `CreateView`, `UpdateView`, and `DeleteView` use `IsAuthenticated` — you must be logged in.

### Authentication

Supported methods:

- **Session**: Log in via Django admin (`/admin/`) — cookies used for API requests.
- **Basic**: Send `Authorization: Basic <base64(username:password)>` header.

## View Configuration

### ListView (`GET /books/`)

- **Permission**: `AllowAny`
- **Filtering** (DjangoFilterBackend):
  - `?title=<partial>` — Title contains (case-insensitive)
  - `?author=<id>` — Filter by author ID
  - `?author__name=<partial>` — Author name contains (case-insensitive)
  - `?publication_year=<YYYY-MM-DD>` — Exact publication date
  - `?publication_year_after=<YYYY-MM-DD>` — Published on or after
  - `?publication_year_before=<YYYY-MM-DD>` — Published on or before
- **Search** (SearchFilter):
  - `?search=<query>` — Searches across title and author name
- **Ordering** (OrderingFilter):
  - `?ordering=title` or `?ordering=-title` — Sort by title (asc/desc)
  - `?ordering=publication_year` or `?ordering=-publication_year` — Sort by date
  - `?ordering=author__name` or `?ordering=-author__name` — Sort by author name
  - Default ordering: by title

### DetailView (`GET /books/<id>/`)

- **Permission**: `AllowAny`
- **Custom behavior**: Uses `select_related('author')` to avoid N+1 queries.

### CreateView (`POST /books/create/`)

- **Permission**: `IsAuthenticated`
- **Validation**: Handled by `BookSerializer` — e.g. `publication_year` cannot be in the future.
- **Hooks**: `perform_create()` — override for logging, notifications, etc.
- **Request body**: `{"title": "...", "publication_year": "YYYY-MM-DD", "author": <author_id>}`

### UpdateView (`GET/PUT/PATCH /books/<id>/update/`)

- **Permission**: `IsAuthenticated`
- **Validation**: Same as create (serializer validates all fields).
- **Hooks**: `perform_update()` — override for auditing, etc.

### DeleteView (`DELETE /books/<id>/delete/`)

- **Permission**: `IsAuthenticated`

## Testing with curl

### 1. List books (no auth)

```bash
curl http://127.0.0.1:8000/books/
```

### 2. Filter, search, and order books

```bash
# Filter by title (partial match)
curl "http://127.0.0.1:8000/books/?title=Pride"

# Filter by author ID
curl "http://127.0.0.1:8000/books/?author=1"

# Filter by author name (partial match)
curl "http://127.0.0.1:8000/books/?author__name=Austen"

# Filter by publication date
curl "http://127.0.0.1:8000/books/?publication_year=1813-01-28"
curl "http://127.0.0.1:8000/books/?publication_year_after=1800-01-01"
curl "http://127.0.0.1:8000/books/?publication_year_before=1850-01-01"

# Search across title and author name
curl "http://127.0.0.1:8000/books/?search=Pride"

# Order results (prefix with - for descending)
curl "http://127.0.0.1:8000/books/?ordering=title"
curl "http://127.0.0.1:8000/books/?ordering=-publication_year"
curl "http://127.0.0.1:8000/books/?ordering=author__name"

# Combine multiple params
curl "http://127.0.0.1:8000/books/?search=Austen&ordering=-publication_year"
```

### 3. Get single book (no auth)

```bash
curl http://127.0.0.1:8000/books/1/
```

### 4. Create book (requires auth)

```bash
curl -X POST http://127.0.0.1:8000/books/create/ ^
  -H "Content-Type: application/json" ^
  -u admin:yourpassword ^
  -d "{\"title\": \"New Book\", \"publication_year\": \"2020-01-01\", \"author\": 1}"
```

### 5. Update book (requires auth)

```bash
curl -X PATCH http://127.0.0.1:8000/books/1/update/ ^
  -H "Content-Type: application/json" ^
  -u admin:yourpassword ^
  -d "{\"title\": \"Updated Title\"}"
```

### 6. Delete book (requires auth)

```bash
curl -X DELETE http://127.0.0.1:8000/books/1/delete/ -u admin:yourpassword
```

### 7. Permission test — create without auth (should fail with 403)

```bash
curl -X POST http://127.0.0.1:8000/books/create/ ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"Test\", \"publication_year\": \"2020-01-01\", \"author\": 1}"
```

---

*Use `\` instead of `^` for line continuation on Linux/macOS.*

## Postman

1. **Import**: Create a new request for each endpoint.
2. **Auth**: For write endpoints, set Auth type to "Basic Auth" and enter credentials.
3. **Body**: For POST/PATCH, use raw JSON with `Content-Type: application/json`.

## Testing

### Test Suite

Unit tests are in `api/test_views.py` and cover:

| Category | Test Cases |
|----------|------------|
| **CRUD** | List (200, data structure), Detail (200, 404), Create (201, validation), Update (200, validation), Delete (204) |
| **Filtering** | title, author, author__name, publication_year, publication_year_after |
| **Search** | search across title and author name |
| **Ordering** | ordering by title, publication_year (asc/desc) |
| **Permissions** | List/Detail allowed without auth; Create/Update/Delete require auth (403 when unauthenticated) |

### Run Tests

```bash
# Run all API view tests
python manage.py test api.test_views

# Run with verbose output
python manage.py test api.test_views -v 2

# Run all tests in the api app
python manage.py test api
```

### Test Environment

- Django uses a separate in-memory SQLite database for tests (no impact on development/production data).
- Each test runs in a transaction that is rolled back after the test.
- `APITestCase` provides `self.client` for making API requests.

### Interpreting Results

- `OK` — All tests passed.
- `FAIL` — A test assertion failed; check the traceback for the failing test and assertion.
- `ERROR` — A test raised an exception before assertions; check the traceback for the cause.

## Run server

```bash
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/`
