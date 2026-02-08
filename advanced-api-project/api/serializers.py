from datetime import date

from rest_framework import serializers

from .models import Author, Book


# ------------------------------------------------------------------------------
# BookListSerializer
# ------------------------------------------------------------------------------
# Minimal serializer for embedding books inside Author (avoids circular nesting).
# ------------------------------------------------------------------------------
class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']


# ------------------------------------------------------------------------------
# AuthorSerializer
# ------------------------------------------------------------------------------
# Purpose: Serializes/deserializes Author model instances for API requests and
# responses. Used when returning author data (e.g., in list/detail views) and
# as a nested representation inside BookSerializer.
# ------------------------------------------------------------------------------
class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    Books = BookListSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'Books']


# ------------------------------------------------------------------------------
# BookSerializer
# ------------------------------------------------------------------------------
# Purpose: Serializes/deserializes Book model instances. Handles the Author-Book
# relationship via nested serialization (see "Relationship handling" below).
#
# Relationship handling (Author <-> Book):
# - Uses AuthorSerializer() as a nested serializer for the 'author' field.
# - On READ (GET): Returns the full author object embedded in each book, e.g.:
#     {"title": "Example", "publication_year": "2020-01-01", "author": {"name": "Jane Doe"}}
# - On WRITE (POST/PUT): Nested writes require custom create()/update() logic.
#   For simple author assignment by ID, use PrimaryKeyRelatedField instead.
# - AuthorSerializer is defined before BookSerializer because it is referenced here.
# ------------------------------------------------------------------------------
class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    publication_year = serializers.DateField() 
    author = AuthorSerializer()

    def validate_publication_year(self, value):
        """Ensure publication_year is not in the future."""
        if value > date.today():
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']
