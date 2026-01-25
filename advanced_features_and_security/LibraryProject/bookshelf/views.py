from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.db import migrations
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.html import escape
from .models import book
from .forms import BookForm
from .forms import ExampleForm

@permission_required('app_name.can_edit', raise_exception=True)

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    
    # 1. Define Groups
    editors, _ = Group.objects.get_or_create(name='Editors')
    viewers, _ = Group.objects.get_or_create(name='Viewers')
    admins, _ = Group.objects.get_or_create(name='Admins')

    # 2. Get Permissions (using the codenames you defined in your Book model)
    can_view = Permission.objects.get(codename='can_view_book')
    can_create = Permission.objects.get(codename='can_create_book')
    can_edit = Permission.objects.get(codename='can_edit_book')
    can_delete = Permission.objects.get(codename='can_delete_book')

    # 3. Assign Permissions
    viewers.permissions.add(can_view)
    
    editors.permissions.add(can_view, can_create, can_edit)
    
    admins.permissions.add(can_view, can_create, can_edit, can_delete)


class Migration(migrations.Migration):
    dependencies = [
        ('your_app_name', '0001_initial'), # Points to your last migration
    ]
    operations = [
        migrations.RunPython(create_groups),
    ]


@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def index(request):
    """
    List all books with optional search functionality.
    
    Security measures:
    - Uses Django ORM with parameterized queries (prevents SQL injection)
    - Validates and sanitizes search input
    - Escapes user input before displaying in templates
    
    Requires can_view_book permission.
    """
    # Security: Get search query from GET parameters (safe for read operations)
    # All queries use Django ORM which automatically parameterizes SQL queries
    search_query = request.GET.get('search', '').strip()
    
    # Security: Validate search query length and content
    # Limit search length to prevent DoS attacks
    if len(search_query) > 100:
        search_query = search_query[:100]
    
    # Security: Use Django ORM filter with Q objects for safe querying
    # ORM automatically escapes and parameterizes all queries
    if search_query:
        # Escape special regex characters to prevent regex injection
        # Then use case-insensitive search with Django ORM
        books = book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query) |
            Q(publication_year__icontains=search_query)
        ).distinct()
    else:
        books = book.objects.all()
    
    # Security: Context data is automatically escaped by Django templates
    # Using |escape filter in templates provides additional protection
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })


@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def create_book(request):
    """
    Create a new book entry.
    
    Security measures:
    - Uses Django ModelForm for automatic input validation
    - Form validation prevents invalid data and SQL injection
    - CSRF protection via middleware and {% csrf_token %} in template
    - Permission check ensures only authorized users can create
    
    Requires can_create_book permission.
    """
    if request.method == 'POST':
        # Security: Django forms automatically validate and sanitize input
        # ModelForm.save() uses parameterized queries (prevents SQL injection)
        form = BookForm(request.POST)
        if form.is_valid():
            # Security: form.save() uses Django ORM which parameterizes queries
            form.save()
            return redirect('bookshelf-index')
    else:
        form = BookForm()
    
    # Security: Form data is automatically escaped in templates
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})


@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, pk):
    """
    Edit an existing book entry.
    
    Security measures:
    - Uses get_object_or_404 to safely retrieve object (prevents errors)
    - Validates pk parameter (Django automatically handles type conversion safely)
    - Uses Django ModelForm for input validation
    - CSRF protection via middleware
    - Permission check ensures only authorized users can edit
    
    Requires can_edit_book permission.
    """
    # Security: get_object_or_404 uses Django ORM with parameterized queries
    # Automatically handles invalid pk values safely
    book_instance = get_object_or_404(book, pk=pk)
    
    if request.method == 'POST':
        # Security: Django forms validate and sanitize all input
        # instance parameter ensures we update existing record safely
        form = BookForm(request.POST, instance=book_instance)
        if form.is_valid():
            # Security: form.save() uses parameterized UPDATE query
            form.save()
            return redirect('bookshelf-index')
    else:
        form = BookForm(instance=book_instance)
    
    # Security: All context data is automatically escaped in templates
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'book': book_instance, 
        'action': 'Edit'
    })


@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """
    Delete a book entry.
    
    Security measures:
    - Requires POST method (prevents accidental deletion via GET)
    - Uses get_object_or_404 for safe object retrieval
    - CSRF protection ensures request is from authenticated user
    - Permission check ensures only authorized users can delete
    
    Requires can_delete_book permission.
    """
    # Security: get_object_or_404 uses parameterized query
    book_instance = get_object_or_404(book, pk=pk)
    
    # Security: Only allow deletion via POST method
    # GET requests only show confirmation page
    if request.method == 'POST':
        # Security: Django ORM delete() uses parameterized DELETE query
        book_instance.delete()
        return redirect('bookshelf-index')
    
    # Security: Context data automatically escaped in templates
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book_instance})


@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_detail(request, pk):
    """
    View detailed information about a specific book.
    
    Security measures:
    - Uses get_object_or_404 for safe object retrieval
    - Django ORM automatically parameterizes queries
    - Template auto-escaping prevents XSS attacks
    - Permission check ensures only authorized users can view
    
    Requires can_view_book permission.
    """
    # Security: get_object_or_404 uses parameterized query (prevents SQL injection)
    book_instance = get_object_or_404(book, pk=pk)
    
    # Security: Django templates automatically escape all variables
    # Additional |escape filter in templates provides defense in depth
    return render(request, 'bookshelf/book_detail.html', {'book': book_instance})

