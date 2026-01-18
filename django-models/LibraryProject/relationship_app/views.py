from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Library, Book

# Create your views here.
class LibrarylistView(ListView, TemplateView):
    model = Library 
    template_name = "relationship_app/library_list.html"

class LibrarydetailView(DetailView, TemplateView):
    model = Library
    template_name = "relationship_app/library_detail.html"


def all_books_view(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


