# Retrieve Operation

## Command
```python
from bookshelf.models import book

# Retrieve and display all attributes of the book with ID=1
# Using Book.objects.get - Django ORM method to retrieve a single object
b = book.objects.get(id=1)
print(f'Retrieved Book - ID: {b.id}, Title: {b.title}, Author: {b.author}, Publication Year: {b.publication_year}')
```

**Key Method:** `Book.objects.get` - This is the Django ORM method used to retrieve a single object from the database.

## Expected Output
```
Retrieved Book - ID: 1, Title: 1984, Author: George Orwell, Publication Year: 1949
```

## Explanation
The `Book.objects.get()` method retrieves a single object from the database that matches the given criteria. In this case, we retrieve the book with `id=1`. The `get()` method raises a `DoesNotExist` exception if no object is found, or a `MultipleObjectsReturned` exception if more than one object matches.

**Method Used:** `Book.objects.get(id=1)`

