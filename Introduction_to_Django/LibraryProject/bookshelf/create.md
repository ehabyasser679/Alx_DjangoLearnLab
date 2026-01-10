# Create Operation

## Command
```python
from bookshelf.models import book

# Create a Book instance with the title "1984", author "George Orwell", and publication year 1949
b = book.objects.create(title='1984', author='George Orwell', publication_year=1949)
print(f'Book created: ID={b.id}, Title={b.title}, Author={b.author}, Year={b.publication_year}')
```

## Expected Output
```
Book created: ID=1, Title=1984, Author=George Orwell, Year=1949
```

## Explanation
The `create()` method is used to create and save a new Book instance in a single step. It returns the created object with its auto-generated primary key (ID). The book is immediately saved to the database.

