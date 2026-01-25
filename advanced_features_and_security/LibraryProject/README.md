# Library Project

A Django application demonstrating advanced features including custom user models, permissions, and group-based access control.

## Features

- Custom User Model with additional fields (email, phone_number, bio, date_of_birth, profile_photo)
- Permission-based access control for book management
- Group-based user roles (Viewers, Editors, Admins)
- CRUD operations with permission enforcement

## Quick Start

### 1. Install Dependencies

```bash
pip install django
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Test Users and Groups

```bash
python manage.py setup_test_users
```

This will create:
- **Viewers group**: Users can only view books
- **Editors group**: Users can view, create, and edit books
- **Admins group**: Users have full access (view, create, edit, delete)

Test users:
- `viewer_user` (password: `viewer123`)
- `editor_user` (password: `editor123`)
- `admin_user` (password: `admin123`)

### 4. Run the Development Server

```bash
python manage.py runserver
```

## Testing Permissions

See [PERMISSIONS_SETUP.md](PERMISSIONS_SETUP.md) for detailed instructions on:
- How permissions are defined
- How to test different user roles
- Troubleshooting common issues

### Quick Test

1. Log in as `viewer_user` and try to access:
   - `/bookshelf/` ✓ (should work - can view)
   - `/bookshelf/create/` ✗ (should get 403 - cannot create)

2. Log in as `editor_user` and try to access:
   - `/bookshelf/create/` ✓ (should work - can create)
   - `/bookshelf/1/delete/` ✗ (should get 403 - cannot delete)

3. Log in as `admin_user`:
   - All operations should work ✓

## Project Structure

- `bookshelf/`: Main app with custom user model and book model
- `relationship_app/`: App demonstrating relationships and permissions
- `LibraryProject/`: Project settings and configuration

## Documentation

- [PERMISSIONS_SETUP.md](PERMISSIONS_SETUP.md) - Complete guide to permissions and groups setup

