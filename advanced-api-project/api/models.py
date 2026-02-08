from django.db import models


# ------------------------------------------------------------------------------
# Author Model
# ------------------------------------------------------------------------------
# Purpose: Represents a person who writes books. Authors are the "one" side of
# the Author-Book relationship. Each Author can have multiple Books associated
# with them (accessed via the reverse relation: author.books.all()).
# ------------------------------------------------------------------------------
class Author(models.Model):
    name = models.CharField(max_length=100)  # The full name of the author


# ------------------------------------------------------------------------------
# Book Model
# ------------------------------------------------------------------------------
# Purpose: Represents a published book. Books are the "many" side of the
# Author-Book relationship. Each Book belongs to exactly one Author via the
# ForeignKey below.
#
# Relationship: Uses ForeignKey to Author, creating a many-to-one relationship.
# - on_delete=CASCADE: When an Author is deleted, all their Books are deleted.
# - related_name='Books': Enables reverse lookup; use author.Books.all() to get
#   all books by an author (note: convention often uses lowercase 'books').
# ------------------------------------------------------------------------------
class Book(models.Model):
    title = models.CharField(max_length=100)  # The title of the book
    publication_year = models.DateField()     # When the book was published
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='Books')
