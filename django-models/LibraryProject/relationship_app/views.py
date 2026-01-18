from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Library, Book, Admin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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
    return render(request, "relationship_app/book_list.html", {"books": books})

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
@admin_required
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
        return render(request, "relationship_app/admin.html", context)
    except Admin.DoesNotExist:
        return HttpResponseForbidden("You do not have permission to access this page. Admin role required.")

