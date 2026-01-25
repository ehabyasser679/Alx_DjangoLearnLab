# CSRF Protection Documentation

This document outlines the CSRF (Cross-Site Request Forgery) protection implementation in the Library Project.

## Overview

All forms in the application are protected against CSRF attacks by including the `{% csrf_token %}` template tag in every form that submits data via POST requests.

## CSRF Protection Implementation

Django's CSRF middleware is enabled by default in `settings.py` (via `CsrfViewMiddleware`). This middleware:
- Generates a unique CSRF token for each user session
- Validates the token on POST requests
- Rejects requests without a valid token

## Protected Forms

All forms in the application include the CSRF token:

### Bookshelf App Templates

1. **`bookshelf/templates/bookshelf/book_form.html`**
   - Used for creating and editing books
   - Includes: `{% csrf_token %}`
   - Location: Line 116

2. **`bookshelf/templates/bookshelf/book_confirm_delete.html`**
   - Used for confirming book deletion
   - Includes: `{% csrf_token %}`
   - Location: Line 106

### Relationship App Templates

1. **`relationship_app/templates/relationship_app/book_form.html`**
   - Used for adding and editing books
   - Includes: `{% csrf_token %}`
   - Location: Line 116

2. **`relationship_app/templates/relationship_app/book_confirm_delete.html`**
   - Used for confirming book deletion
   - Includes: `{% csrf_token %}`
   - Location: Line 105

3. **`relationship_app/templates/relationship_app/register.html`**
   - User registration form
   - Includes: `{% csrf_token %}`
   - Location: Line 13

4. **`relationship_app/templates/relationship_app/login.html`**
   - User login form
   - Includes: `{% csrf_token %}`
   - Location: Line 13

## Template Syntax

All forms follow this pattern:

```html
<form method="post">
    {% csrf_token %}
    <!-- Form fields here -->
    <button type="submit">Submit</button>
</form>
```

The `{% csrf_token %}` tag generates a hidden input field with the CSRF token:
```html
<input type="hidden" name="csrfmiddlewaretoken" value="...">
```

## How CSRF Protection Works

1. **Token Generation**: When a user visits a page with a form, Django generates a unique CSRF token tied to their session.

2. **Token Inclusion**: The `{% csrf_token %}` template tag inserts a hidden input field containing the token into the form.

3. **Token Validation**: When the form is submitted via POST:
   - Django's CSRF middleware extracts the token from the request
   - It compares it with the token stored in the user's session
   - If tokens match, the request is processed
   - If tokens don't match or are missing, Django returns a 403 Forbidden error

## Security Benefits

- **Prevents CSRF Attacks**: Malicious websites cannot submit forms on behalf of authenticated users
- **Session-Based**: Tokens are tied to user sessions, making them difficult to forge
- **Automatic Validation**: Django handles validation automatically via middleware

## Testing CSRF Protection

### Manual Testing

1. **Normal Form Submission**:
   - Fill out and submit a form normally
   - Should work without errors

2. **Missing Token Test**:
   - Remove `{% csrf_token %}` from a form template
   - Submit the form
   - Should receive a 403 Forbidden error: "CSRF verification failed"

3. **Invalid Token Test**:
   - Manually modify the CSRF token value in the form
   - Submit the form
   - Should receive a 403 Forbidden error

### Automated Testing

Django's test client automatically handles CSRF tokens, but you can test CSRF protection explicitly:

```python
from django.test import Client
from django.urls import reverse

def test_csrf_protection(self):
    client = Client(enforce_csrf_checks=True)
    # Attempt POST without CSRF token
    response = client.post(reverse('bookshelf-create'), {})
    self.assertEqual(response.status_code, 403)
```

## Best Practices

1. **Always Include CSRF Token**: Every form that uses POST method must include `{% csrf_token %}`

2. **Place Token Early**: Place `{% csrf_token %}` immediately after the opening `<form>` tag

3. **Use POST for State Changes**: Use POST method for any action that changes server state (create, update, delete)

4. **GET for Safe Operations**: Use GET method only for safe, read-only operations

5. **Exempt Only When Necessary**: Avoid using `@csrf_exempt` decorator unless absolutely necessary

## Exemptions (Not Recommended)

If you need to exempt a view from CSRF protection (rare cases), use:

```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_view(request):
    # This view is NOT protected against CSRF attacks
    pass
```

**Warning**: Only use `@csrf_exempt` for views that are intentionally designed to accept requests from external sources (e.g., API endpoints with alternative authentication).

## Troubleshooting

### Issue: "CSRF verification failed. Request aborted."

**Possible Causes:**
1. Missing `{% csrf_token %}` in the form template
2. Form submitted from a different domain
3. Session expired
4. CSRF middleware not enabled

**Solutions:**
1. Verify `{% csrf_token %}` is present in the form
2. Check that `CsrfViewMiddleware` is in `MIDDLEWARE` in `settings.py`
3. Ensure cookies are enabled in the browser
4. Check that the form is being submitted to the same domain

### Issue: Token Mismatch

**Possible Causes:**
1. Multiple tabs/windows with different sessions
2. Session expired between page load and form submission
3. Browser blocking cookies

**Solutions:**
1. Refresh the page to get a new token
2. Clear browser cookies and try again
3. Ensure cookies are enabled

## Verification Checklist

- [x] All POST forms include `{% csrf_token %}`
- [x] CSRF middleware is enabled in settings
- [x] Forms use POST method for state-changing operations
- [x] No views use `@csrf_exempt` unnecessarily
- [x] All templates tested for CSRF protection

## Summary

All forms in the Library Project are protected against CSRF attacks through:
- Django's built-in CSRF middleware
- `{% csrf_token %}` template tag in all forms
- Automatic validation on POST requests

This ensures that malicious websites cannot perform unauthorized actions on behalf of authenticated users.

