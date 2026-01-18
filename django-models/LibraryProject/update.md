# Update Operation

## Command
```python
from bookshelf.models import book

# Update the title of "1984" to "Nineteen Eighty-Four" and save the changes
b = book.objects.get(id=1)
# Using book.title to update the title attribute
b.title = 'Nineteen Eighty-Four'
b.save()
print(f'Book updated - ID: {b.id}, New Title: {b.title}, Author: {b.author}, Publication Year: {b.publication_year}')
```

**Key Attribute:** `book.title` - This attribute is used to update the title of the book instance.

## Expected Output
```
Book updated - ID: 1, New Title: Nineteen Eighty-Four, Author: George Orwell, Publication Year: 1949
```

## Explanation
To update a model instance, you first retrieve it using `get()`, modify its attributes (such as `book.title`), and then call the `save()` method to persist the changes to the database. The `save()` method updates the existing record in the database.

**Attribute Used:** `book.title = 'Nineteen Eighty-Four'` - This updates the title attribute of the book instance.

