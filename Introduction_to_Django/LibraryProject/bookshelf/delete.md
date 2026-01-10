# Delete Operation

## Command
```python
from bookshelf.models import book

# Delete the book you created and confirm the deletion by trying to retrieve all books again
b = book.objects.get(id=1)
print(f'Deleting book: {b.title}')
b.delete()
print('Book deleted successfully')

# Confirm deletion by checking all books
all_books = book.objects.all()
print(f'Total books remaining: {all_books.count()}')
```

## Expected Output
```
Deleting book: Nineteen Eighty-Four
Book deleted successfully
Total books remaining: 0
```

## Explanation
The `delete()` method removes the object from the database. After deletion, the object still exists in Python memory but is no longer in the database. To confirm the deletion, we use `objects.all()` to retrieve all books and `count()` to verify that no books remain in the database.

