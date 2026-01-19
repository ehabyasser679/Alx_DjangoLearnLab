from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Library, Book, Admin, Librarian, Member, Author, LibraryBook
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden
from django.forms import ModelForm
from functools import wraps

# Create your views here.
class LibrarylistView(ListView, TemplateView):
    model = Library 
    template_name = "relationship_app/library_list.html"

class LibrarydetailView(DetailView, TemplateView):
    model = Library
    template_name = "relationship_app/library_detail.html"

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("library-list")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

def all_books_view(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Test functions for user_passes_test decorator
def is_admin(user):
    """Check if user has Admin role"""
    if not user.is_authenticated:
        return False
    return Admin.objects.filter(user=user).exists()

def is_librarian(user):
    """Check if user has Librarian role"""
    if not user.is_authenticated:
        return False
    return Librarian.objects.filter(name=user.username).exists()

def is_member(user):
    """Check if user has Member role"""
    if not user.is_authenticated:
        return False
    return Member.objects.filter(user=user).exists()

def admin_required(view_func):
    """Decorator to check if user has Admin role"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            admin_instance = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            return HttpResponseForbidden("You do not have permission to access this page. Admin role required.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    """Admin view that only users with Admin role can access"""
    try:
        admin_instance = Admin.objects.get(user=request.user)
        libraries = Library.objects.all()
        books = Book.objects.all()
        context = {
            'admin': admin_instance,
            'libraries': libraries,
            'books': books,
            'total_libraries': libraries.count(),
            'total_books': books.count(),
        }
        return render(request, "relationship_app/admin_view.html", context)
    except Admin.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page. Admin role required.")

def librarian_required(view_func):
    """Decorator to check if user has Librarian role"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            # Librarian model uses name field, so we check by matching username with name
            librarian_instance = Librarian.objects.get(name=request.user.username)
        except Librarian.DoesNotExist:
            return HttpResponseForbidden("You do not have permission to access this page. Librarian role required.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian view that only users with Librarian role can access"""
    try:
        # Librarian model uses name field, so we check by matching username with name
        librarian_instance = Librarian.objects.get(name=request.user.username)
        library = librarian_instance.library
        library_books = library.books.all()
        authors = Author.objects.filter(book__in=library_books).distinct()
        
        # Get LibraryBook instances to access date_added
        library_book_instances = LibraryBook.objects.filter(library=library).select_related('book')
        
        context = {
            'librarian': librarian_instance,
            'library': library,
            'library_books': library_books,
            'library_book_instances': library_book_instances,
            'library_books_count': library_books.count(),
            'authors_count': authors.count(),
        }
        return render(request, "relationship_app/librarian_view.html", context)
    except Librarian.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page. Librarian role required.")

def member_required(view_func):
    """Decorator to check if user has Member role"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            member_instance = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            return HttpResponseForbidden("You do not have permission to access this page. Member role required.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@user_passes_test(is_member)
def member_view(request):
    """Member view that only users with Member role can access"""
    try:
        member_instance = Member.objects.get(user=request.user)
        library = member_instance.library
        library_books = library.books.all()
        
        context = {
            'member': member_instance,
            'library': library,
            'library_books': library_books,
            'library_books_count': library_books.count(),
        }
        return render(request, "relationship_app/member_view.html", context)
    except Member.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page. Member role required.")

# Form for Book model
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book - requires can_add_book permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book-list')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add'})

@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """View to edit an existing book - requires can_change_book permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'book': book, 'action': 'Edit'})

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})


