from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Library

# Create your views here.
class LibrarylistView(ListView, TemplateView):
    model = Library 
    template_name = "relationship_app/list.html"

class LibrarydetailView(DetailView, TemplateView):
    model = Library
    template_name = "relationship_app/detail.html"

