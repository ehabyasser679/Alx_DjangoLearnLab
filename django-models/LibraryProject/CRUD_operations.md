# CRUD Operations Documentation

This document contains all Create, Read, Update, and Delete (CRUD) operations performed on the Book model in the Django shell.

---

## 1. CREATE Operation

### Command
```python
from bookshelf.models import book

# Create a Book instance with the title "1984", author "George Orwell", and publication year 1949
# Using Book.objects.create - Django ORM method to create and save a new instance
b = book.objects.create(title='1984', author='George Orwell', publication_year=1949)
print(f'Book created: ID={b.id}, Title={b.title}, Author={b.author}, Year={b.publication_year}')
```

### Output
```
Book created: ID=1, Title=1984, Author=George Orwell, Year=1949
```

### Explanation
The `Book.objects.create()` method is used to create and save a new Book instance in a single step. It returns the created object with its auto-generated primary key (ID). The book is immediately saved to the database.

**Method Used:** `Book.objects.create(title='1984', author='George Orwell', publication_year=1949)`

---

## 2. RETRIEVE Operation

### Command
```python
from bookshelf.models import book

# Retrieve and display all attributes of the book with ID=1
b = book.objects.get(id=1)
print(f'Retrieved Book - ID: {b.id}, Title: {b.title}, Author: {b.author}, Publication Year: {b.publication_year}')
```

### Output
```
Retrieved Book - ID: 1, Title: 1984, Author: George Orwell, Publication Year: 1949
```

### Explanation
The `get()` method retrieves a single object from the database that matches the given criteria. In this case, we retrieve the book with `id=1`. The `get()` method raises a `DoesNotExist` exception if no object is found, or a `MultipleObjectsReturned` exception if more than one object matches.

---

## 3. UPDATE Operation

### Command
```python
from bookshelf.models import book

# Update the title of "1984" to "Nineteen Eighty-Four" and save the changes
b = book.objects.get(id=1)
b.title = 'Nineteen Eighty-Four'
b.save()
print(f'Book updated - ID: {b.id}, New Title: {b.title}, Author: {b.author}, Publication Year: {b.publication_year}')
```

### Output
```
Book updated - ID: 1, New Title: Nineteen Eighty-Four, Author: George Orwell, Publication Year: 1949
```

### Explanation
To update a model instance, you first retrieve it using `get()`, modify its attributes, and then call the `save()` method to persist the changes to the database. The `save()` method updates the existing record in the database.

---

## 4. DELETE Operation

### Command
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

### Output
```
Deleting book: Nineteen Eighty-Four
Book deleted successfully
Total books remaining: 0
```

### Explanation
The `delete()` method removes the object from the database. After deletion, the object still exists in Python memory but is no longer in the database. To confirm the deletion, we use `objects.all()` to retrieve all books and `count()` to verify that no books remain in the database.

---

## Summary

All CRUD operations were successfully performed:
- ✅ **Create**: Successfully created a book with ID=1
- ✅ **Retrieve**: Successfully retrieved the book and displayed all its attributes
- ✅ **Update**: Successfully updated the book title from "1984" to "Nineteen Eighty-Four"
- ✅ **Delete**: Successfully deleted the book and confirmed deletion (0 books remaining)

