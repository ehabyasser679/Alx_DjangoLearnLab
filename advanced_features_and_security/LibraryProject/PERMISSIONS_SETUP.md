# Permissions and Groups Setup Guide

This document explains how permissions and groups are set up and used in the Library Project application.

## Overview

The application uses Django's built-in permission system to control access to different operations on book models. Permissions are assigned to groups, and users are assigned to groups to inherit those permissions.

## Permission Definitions

### Bookshelf App Permissions

The `book` model in the `bookshelf` app defines the following custom permissions:

- **`can_view_book`**: Allows users to view book details and list books
- **`can_create_book`**: Allows users to create new book entries
- **`can_edit_book`**: Allows users to edit existing book details
- **`can_delete_book`**: Allows users to delete book entries

### Relationship App Permissions

The `Book` model in the `relationship_app` defines the following custom permissions:

- **`can_add_book`**: Allows users to add new books
- **`can_change_book`**: Allows users to modify existing books
- **`can_delete_book`**: Allows users to delete books

## Groups

Three groups are created to organize users by their access levels:

### 1. Viewers Group
- **Permissions**: `can_view_book`
- **Capabilities**: 
  - Can view book lists
  - Can view book details
  - Cannot create, edit, or delete books

### 2. Editors Group
- **Permissions**: `can_view_book`, `can_create_book`, `can_edit_book`
- **Also includes**: `can_add_book`, `can_change_book` (from relationship_app)
- **Capabilities**:
  - Can view book lists and details
  - Can create new books
  - Can edit existing books
  - Cannot delete books

### 3. Admins Group
- **Permissions**: `can_view_book`, `can_create_book`, `can_edit_book`, `can_delete_book`
- **Also includes**: `can_add_book`, `can_change_book`, `can_delete_book` (from relationship_app)
- **Capabilities**:
  - Full access: view, create, edit, and delete books

## Setup Instructions

### 1. Run Migrations

First, ensure all migrations are applied:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the permission objects in the database.

### 2. Create Test Users and Groups

Use the management command to automatically set up test users and groups:

```bash
python manage.py setup_test_users
```

This command will:
- Create three groups: Viewers, Editors, Admins
- Create three test users assigned to each group
- Assign appropriate permissions to each group

**Test Users Created:**
- `viewer_user` (password: `viewer123`) - Assigned to Viewers group
- `editor_user` (password: `editor123`) - Assigned to Editors group
- `admin_user` (password: `admin123`) - Assigned to Admins group

### 3. Reset Test Data (Optional)

To delete and recreate test users and groups:

```bash
python manage.py setup_test_users --reset
```

## Manual Setup (Alternative)

If you prefer to set up groups and permissions manually through the Django admin:

1. Go to Django admin panel
2. Navigate to **Groups** under **Authentication and Authorization**
3. Create groups: Viewers, Editors, Admins
4. Assign permissions to each group:
   - **Viewers**: Select `bookshelf | book | Can view book details`
   - **Editors**: Select `bookshelf | book | Can view book details`, `Can create a new book entry`, `Can edit existing book details`
   - **Admins**: Select all book permissions
5. Create users and assign them to appropriate groups

## Permission Enforcement in Views

Permissions are enforced using Django decorators in the views:

### Bookshelf App Views

```python
@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def index(request):
    # List all books

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def create_book(request):
    # Create a new book

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, pk):
    # Edit an existing book

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    # Delete a book
```

### Relationship App Views

```python
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    # Add a new book

@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    # Edit an existing book

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    # Delete a book
```

The `raise_exception=True` parameter ensures that users without the required permission receive an HTTP 403 Forbidden response instead of being redirected to a login page.

## Testing Permissions

### Test Procedure

1. **Log in as viewer_user**:
   - Should be able to view book lists and details
   - Should NOT be able to access create, edit, or delete URLs (will get 403 Forbidden)

2. **Log in as editor_user**:
   - Should be able to view, create, and edit books
   - Should NOT be able to delete books (will get 403 Forbidden)

3. **Log in as admin_user**:
   - Should have full access to all operations: view, create, edit, and delete

### Testing URLs

**Bookshelf App:**
- List: `/bookshelf/` (requires `can_view_book`)
- Create: `/bookshelf/create/` (requires `can_create_book`)
- Detail: `/bookshelf/<id>/` (requires `can_view_book`)
- Edit: `/bookshelf/<id>/edit/` (requires `can_edit_book`)
- Delete: `/bookshelf/<id>/delete/` (requires `can_delete_book`)

**Relationship App:**
- List: `/relationship_app/books/` (login required)
- Add: `/relationship_app/add_book/` (requires `can_add_book`)
- Edit: `/relationship_app/edit_book/<id>/` (requires `can_change_book`)
- Delete: `/relationship_app/books/<id>/delete/` (requires `can_delete_book`)

## Permission Variable Names

The following variable names are used throughout the codebase:

**Bookshelf App:**
- `can_view_book`
- `can_create_book`
- `can_edit_book`
- `can_delete_book`

**Relationship App:**
- `can_add_book`
- `can_change_book`
- `can_delete_book`

These names match the permission codenames defined in the model `Meta` classes.

## Troubleshooting

### Permission Not Found Error

If you get a `Permission.DoesNotExist` error:
1. Ensure migrations have been run: `python manage.py migrate`
2. Check that permissions are defined in the model's `Meta.permissions`
3. Verify the app name and permission codename match exactly

### User Can't Access View Despite Having Permission

1. Check that the user is assigned to the correct group
2. Verify the group has the required permission
3. Ensure the user is logged in (`@login_required` decorator)
4. Check that the permission string in the decorator matches exactly: `'app_name.permission_codename'`

### Resetting Permissions

To reset all test data and start fresh:

```bash
python manage.py setup_test_users --reset
```

## Additional Notes

- Superusers automatically have all permissions and can bypass permission checks
- Permissions are checked at the view level using decorators
- The `@login_required` decorator must be used before `@permission_required` for proper authentication flow
- Groups can have multiple permissions assigned
- Users can belong to multiple groups and will inherit permissions from all groups

