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
# relationship: nested author on READ, author ID on WRITE for form submissions.
#
# Relationship handling (Author <-> Book):
# - READ: Returns full author object via to_representation().
# - WRITE: Accepts author by ID (PrimaryKeyRelatedField) for create/update.
# ------------------------------------------------------------------------------
class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    publication_year = serializers.DateField()
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=False,
    )

    def to_representation(self, instance):
        """Return nested author object on read for richer API responses."""
        rep = super().to_representation(instance)
        rep['author'] = AuthorSerializer(instance.author).data
        return rep

    def validate_publication_year(self, value):
        """Ensure publication_year is not in the future."""
        if value > date.today():
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
