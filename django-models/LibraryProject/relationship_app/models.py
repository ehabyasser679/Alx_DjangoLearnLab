from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class LibraryBook(models.Model):
    library = models.ForeignKey('Library', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, through='LibraryBook')

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
