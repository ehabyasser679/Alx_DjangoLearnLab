from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Library, Book
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class LibrarylistView(ListView, TemplateView):
    model = Library 
    template_name = "relationship_app/library_list.html"

class LibrarydetailView(DetailView, TemplateView):
    model = Library
    template_name = "relationship_app/library_detail.html"

def login_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("library-list")
    return render(request, "relationship_app/login.html", {"form": form})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("library-list")
    return render(request, "relationship_app/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def all_books_view(request):
    books = Book.objects.all()
    return render(request, "relationship_app/book_list.html", {"books": books})

