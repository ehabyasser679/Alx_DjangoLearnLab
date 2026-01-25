# Testing Guide for Permissions

This guide provides step-by-step instructions for manually testing the permission system.

## Prerequisites

1. Run migrations: `python manage.py migrate`
2. Set up test users: `python manage.py setup_test_users`
3. Start the development server: `python manage.py runserver`

## Test Users

| Username | Password | Group | Permissions |
|----------|----------|-------|-------------|
| viewer_user | viewer123 | Viewers | can_view_book only |
| editor_user | editor123 | Editors | can_view_book, can_create_book, can_edit_book |
| admin_user | admin123 | Admins | All permissions (view, create, edit, delete) |

## Test Scenarios

### Test 1: Viewer User (Limited Access)

**Objective**: Verify that viewer_user can only view books, not modify them.

1. **Log in as viewer_user**:
   - Go to `/login/`
   - Username: `viewer_user`
   - Password: `viewer123`

2. **Test View Access** (Should Work):
   - Navigate to `/bookshelf/`
   - ✅ Should see the book list
   - Navigate to `/bookshelf/1/` (if a book exists)
   - ✅ Should see book details

3. **Test Create Access** (Should Fail):
   - Navigate to `/bookshelf/create/`
   - ❌ Should receive HTTP 403 Forbidden error
   - Message: "Permission denied"

4. **Test Edit Access** (Should Fail):
   - Navigate to `/bookshelf/1/edit/` (if a book exists)
   - ❌ Should receive HTTP 403 Forbidden error

5. **Test Delete Access** (Should Fail):
   - Navigate to `/bookshelf/1/delete/` (if a book exists)
   - ❌ Should receive HTTP 403 Forbidden error

**Expected Result**: Viewer can only view books, all modification attempts result in 403 errors.

---

### Test 2: Editor User (Moderate Access)

**Objective**: Verify that editor_user can view, create, and edit books, but cannot delete them.

1. **Log out and log in as editor_user**:
   - Go to `/logout/` then `/login/`
   - Username: `editor_user`
   - Password: `editor123`

2. **Test View Access** (Should Work):
   - Navigate to `/bookshelf/`
   - ✅ Should see the book list

3. **Test Create Access** (Should Work):
   - Navigate to `/bookshelf/create/`
   - ✅ Should see the create book form
   - Fill in the form and submit
   - ✅ Should successfully create a book

4. **Test Edit Access** (Should Work):
   - Navigate to `/bookshelf/1/edit/` (use an existing book ID)
   - ✅ Should see the edit form
   - Modify fields and submit
   - ✅ Should successfully update the book

5. **Test Delete Access** (Should Fail):
   - Navigate to `/bookshelf/1/delete/` (use an existing book ID)
   - ❌ Should receive HTTP 403 Forbidden error

**Expected Result**: Editor can view, create, and edit books, but cannot delete them.

---

### Test 3: Admin User (Full Access)

**Objective**: Verify that admin_user has full access to all operations.

1. **Log out and log in as admin_user**:
   - Go to `/logout/` then `/login/`
   - Username: `admin_user`
   - Password: `admin123`

2. **Test All Operations** (Should All Work):
   - View: `/bookshelf/` ✅
   - Create: `/bookshelf/create/` ✅
   - Edit: `/bookshelf/1/edit/` ✅
   - Delete: `/bookshelf/1/delete/` ✅

**Expected Result**: Admin can perform all operations without any 403 errors.

---

### Test 4: Relationship App Permissions

**Objective**: Test permissions in the relationship_app.

1. **Log in as viewer_user**:
   - Navigate to `/relationship_app/books/`
   - ✅ Should see the book list (login required only)
   - Navigate to `/relationship_app/add_book/`
   - ❌ Should receive HTTP 403 Forbidden (requires `can_add_book`)

2. **Log in as editor_user**:
   - Navigate to `/relationship_app/add_book/`
   - ✅ Should see the add book form (has `can_add_book`)
   - Navigate to `/relationship_app/edit_book/1/`
   - ✅ Should see the edit form (has `can_change_book`)
   - Navigate to `/relationship_app/books/1/delete/`
   - ❌ Should receive HTTP 403 Forbidden (does not have `can_delete_book`)

3. **Log in as admin_user**:
   - All relationship_app operations should work ✅

---

## Testing Checklist

Use this checklist to ensure all permissions are working correctly:

### Bookshelf App

- [ ] viewer_user can view book list
- [ ] viewer_user can view book details
- [ ] viewer_user cannot create books (403 error)
- [ ] viewer_user cannot edit books (403 error)
- [ ] viewer_user cannot delete books (403 error)
- [ ] editor_user can view books
- [ ] editor_user can create books
- [ ] editor_user can edit books
- [ ] editor_user cannot delete books (403 error)
- [ ] admin_user can perform all operations

### Relationship App

- [ ] viewer_user can view book list (login required)
- [ ] viewer_user cannot add books (403 error)
- [ ] editor_user can add books
- [ ] editor_user can edit books
- [ ] editor_user cannot delete books (403 error)
- [ ] admin_user can perform all operations

## Common Issues and Solutions

### Issue: Permission Denied Even Though User Has Permission

**Solution**:
1. Verify the user is assigned to the correct group
2. Check that the group has the required permission
3. Ensure you're using the correct permission codename in the decorator
4. Try logging out and logging back in (permissions are cached)

### Issue: User Can Access View Without Permission

**Solution**:
1. Check if the user is a superuser (superusers bypass permissions)
2. Verify the `@permission_required` decorator is correctly applied
3. Ensure `raise_exception=True` is set in the decorator

### Issue: Management Command Fails

**Solution**:
1. Ensure migrations have been run: `python manage.py migrate`
2. Check that permissions are defined in the model's `Meta.permissions`
3. Verify the app name matches exactly (case-sensitive)

## Resetting Test Data

To reset all test users and groups:

```bash
python manage.py setup_test_users --reset
```

This will delete existing test users and groups and recreate them with fresh data.

## Automated Testing

For automated testing, you can create Django test cases. See the `tests.py` files in each app for examples.

## Notes

- All test users have simple passwords for testing purposes only
- In production, use strong passwords and proper password policies
- Superusers automatically have all permissions
- Permissions are checked at the view level, not at the template level

