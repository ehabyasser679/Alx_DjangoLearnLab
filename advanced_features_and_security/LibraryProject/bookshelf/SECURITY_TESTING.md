# Security Testing Guide for Bookshelf App

This guide provides step-by-step procedures for testing the security measures implemented in the bookshelf application.

## Prerequisites

1. Start the development server: `python manage.py runserver`
2. Create test users: `python manage.py setup_test_users`
3. Have a browser with developer tools (Chrome DevTools, Firefox DevTools)
4. Optional: Use tools like Burp Suite or OWASP ZAP for advanced testing

## Testing Checklist

- [ ] SQL Injection Prevention
- [ ] Input Validation
- [ ] CSRF Protection
- [ ] XSS Prevention
- [ ] Content Security Policy
- [ ] Authentication and Authorization
- [ ] Security Headers

---

## 1. SQL Injection Testing

### Test 1: Search Field SQL Injection Attempt

**Objective**: Verify that SQL injection attempts in search are blocked.

**Steps**:
1. Log in as any user
2. Navigate to `/bookshelf/`
3. In the search field, enter: `' OR '1'='1`
4. Click Search

**Expected Result**: 
- ✅ Search should work normally
- ✅ No SQL errors should occur
- ✅ Results should be empty or show matching books (not all books)
- ✅ Check browser console and server logs for SQL errors (should be none)

**Why This Works**: Django ORM automatically parameterizes queries, so the single quote is treated as a literal character, not SQL syntax.

### Test 2: Primary Key SQL Injection

**Objective**: Verify that primary key parameters are safely handled.

**Steps**:
1. Log in as any user
2. Try to access: `/bookshelf/1' OR '1'='1/`

**Expected Result**:
- ✅ Should return 404 (invalid primary key)
- ✅ No SQL errors in logs
- ✅ No database information leaked

**Why This Works**: `get_object_or_404()` uses parameterized queries and validates the pk type.

### Test 3: Union-Based SQL Injection

**Objective**: Test for union-based SQL injection vulnerabilities.

**Steps**:
1. In search field, enter: `' UNION SELECT * FROM book --`
2. Click Search

**Expected Result**:
- ✅ Search should handle input safely
- ✅ No SQL errors
- ✅ Results should be empty or normal search results

---

## 2. Input Validation Testing

### Test 1: Extremely Long Input

**Objective**: Verify input length limits prevent DoS attacks.

**Steps**:
1. Navigate to create book form: `/bookshelf/create/`
2. Enter a title with 1000+ characters
3. Submit the form

**Expected Result**:
- ✅ Form should validate and reject input
- ✅ Error message should appear
- ✅ Input should be truncated to max length (200 characters)

### Test 2: Invalid Publication Year

**Objective**: Verify year validation works.

**Steps**:
1. Navigate to create book form
2. Enter publication year: `999` or `3000`
3. Submit the form

**Expected Result**:
- ✅ Form validation should fail
- ✅ Error message: "Publication year must be between 1000 and [current year + 1]"
- ✅ Book should not be created

### Test 3: Empty Required Fields

**Objective**: Verify required field validation.

**Steps**:
1. Navigate to create book form
2. Leave title or author empty
3. Submit the form

**Expected Result**:
- ✅ Form validation should fail
- ✅ Error messages should appear
- ✅ Book should not be created

### Test 4: Special Characters in Input

**Objective**: Verify special characters are handled safely.

**Steps**:
1. Create a book with title: `<script>alert('XSS')</script>`
2. Submit the form

**Expected Result**:
- ✅ Book should be created (special characters are allowed in titles)
- ✅ When viewing the book, the script should NOT execute
- ✅ The title should be displayed as text, not executed as code

---

## 3. CSRF Protection Testing

### Test 1: Missing CSRF Token

**Objective**: Verify forms require CSRF tokens.

**Steps**:
1. Log in as any user
2. Navigate to create book form: `/bookshelf/create/`
3. Open browser developer tools (F12)
4. Find the form in the HTML
5. Remove or modify the CSRF token input field
6. Submit the form

**Expected Result**:
- ✅ Form submission should fail
- ✅ Error: "CSRF verification failed"
- ✅ HTTP 403 Forbidden response
- ✅ Book should not be created

### Test 2: Invalid CSRF Token

**Objective**: Verify invalid tokens are rejected.

**Steps**:
1. Log in and navigate to create book form
2. Open developer tools
3. Change the CSRF token value to something invalid
4. Submit the form

**Expected Result**:
- ✅ Form submission should fail
- ✅ CSRF verification error
- ✅ HTTP 403 response

### Test 3: CSRF Token Expiration

**Objective**: Verify expired tokens are rejected.

**Steps**:
1. Log in and open create book form
2. Wait for session to expire (or manually expire session)
3. Submit the form

**Expected Result**:
- ✅ Form submission should fail
- ✅ CSRF verification error
- ✅ User may be redirected to login

---

## 4. XSS (Cross-Site Scripting) Testing

### Test 1: Stored XSS in Title

**Objective**: Verify XSS payloads in book titles are escaped.

**Steps**:
1. Create a book with title: `<script>alert('XSS')</script>`
2. View the book list
3. Check if the script executes

**Expected Result**:
- ✅ Script should NOT execute
- ✅ Title should be displayed as plain text: `<script>alert('XSS')</script>`
- ✅ Browser console should show no errors
- ✅ Check page source: script tags should be HTML-escaped

### Test 2: Reflected XSS in Search

**Objective**: Verify search input is properly escaped.

**Steps**:
1. In search field, enter: `<img src=x onerror=alert('XSS')>`
2. Click Search
3. Check if the image/script executes

**Expected Result**:
- ✅ Script should NOT execute
- ✅ Search query should be displayed as text
- ✅ No images should load
- ✅ Check page source: input should be escaped

### Test 3: XSS in URL Parameters

**Objective**: Verify URL parameters are safe.

**Steps**:
1. Navigate to: `/bookshelf/?search=<script>alert('XSS')</script>`
2. Check if script executes

**Expected Result**:
- ✅ Script should NOT execute
- ✅ Search query should be escaped in the input field
- ✅ No JavaScript execution

---

## 5. Content Security Policy Testing

### Test 1: Verify CSP Headers

**Objective**: Verify CSP headers are present in responses.

**Steps**:
1. Open browser developer tools (F12)
2. Go to Network tab
3. Navigate to any page: `/bookshelf/`
4. Click on the request in Network tab
5. Check Response Headers

**Expected Result**:
- ✅ `Content-Security-Policy` header should be present
- ✅ Header should contain directives like: `default-src 'self'`
- ✅ `frame-ancestors 'none'` should be present

### Test 2: Test CSP Enforcement

**Objective**: Verify CSP blocks unauthorized scripts.

**Steps**:
1. Open browser console
2. Try to inject a script tag via console: `document.createElement('script')`
3. Check for CSP violations

**Expected Result**:
- ✅ Browser should log CSP violations in console
- ✅ Unauthorized scripts should be blocked
- ✅ Check console for messages like: "Refused to execute inline script"

### Test 3: Test Frame Embedding

**Objective**: Verify clickjacking protection.

**Steps**:
1. Create an HTML file with an iframe:
```html
<iframe src="http://localhost:8000/bookshelf/"></iframe>
```
2. Open the HTML file in a browser

**Expected Result**:
- ✅ Page should NOT load in iframe
- ✅ Browser console may show CSP violation
- ✅ This prevents clickjacking attacks

---

## 6. Authentication and Authorization Testing

### Test 1: Unauthenticated Access

**Objective**: Verify unauthenticated users cannot access views.

**Steps**:
1. Log out (or use incognito/private window)
2. Try to access: `/bookshelf/`

**Expected Result**:
- ✅ Should redirect to login page
- ✅ Should not show book list

### Test 2: Unauthorized Permission Access

**Objective**: Verify users without permissions cannot access protected views.

**Steps**:
1. Log in as `viewer_user` (only has view permission)
2. Try to access: `/bookshelf/create/`

**Expected Result**:
- ✅ Should return HTTP 403 Forbidden
- ✅ Error message: "Permission denied"
- ✅ Should not show create form

### Test 3: Permission Bypass Attempt

**Objective**: Verify permission checks cannot be bypassed.

**Steps**:
1. Log in as `viewer_user`
2. Try to directly POST to: `/bookshelf/create/` (bypassing form)

**Expected Result**:
- ✅ Should return HTTP 403 Forbidden
- ✅ Book should not be created
- ✅ Permission check should occur before processing

---

## 7. Security Headers Testing

### Test 1: Verify All Security Headers

**Objective**: Verify all security headers are present.

**Steps**:
1. Open developer tools → Network tab
2. Navigate to any page
3. Check Response Headers

**Expected Headers**:
- ✅ `X-Content-Type-Options: nosniff`
- ✅ `X-Frame-Options: DENY`
- ✅ `X-XSS-Protection: 1; mode=block`
- ✅ `Content-Security-Policy: ...`

### Test 2: Test X-Frame-Options

**Objective**: Verify clickjacking protection.

**Steps**:
1. Create HTML file with iframe (as in CSP Test 3)
2. Try to embed the page

**Expected Result**:
- ✅ Page should not load in iframe
- ✅ `X-Frame-Options: DENY` should prevent embedding

---

## Automated Testing

### Using Django Test Framework

Create test cases in `bookshelf/tests.py`:

```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import book

User = get_user_model()

class SecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(email='test@example.com', password='testpass123')
    
    def test_sql_injection_in_search(self):
        """Test that SQL injection in search is prevented"""
        response = self.client.get('/bookshelf/', {'search': "' OR '1'='1"})
        self.assertEqual(response.status_code, 200)
        # Should not raise any database errors
    
    def test_xss_in_title(self):
        """Test that XSS in title is escaped"""
        book.objects.create(
            title="<script>alert('XSS')</script>",
            author="Test Author",
            publication_year=2023
        )
        response = self.client.get('/bookshelf/')
        self.assertNotIn('<script>', response.content.decode())
        self.assertIn('&lt;script&gt;', response.content.decode())
    
    def test_csrf_protection(self):
        """Test that CSRF protection is enabled"""
        response = self.client.post('/bookshelf/create/', {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2023
        }, enforce_csrf_checks=True)
        # Should fail without proper CSRF token
        self.assertIn(response.status_code, [403, 400])
```

## Tools for Advanced Testing

### Browser Extensions

- **OWASP ZAP**: Automated security scanner
- **Burp Suite**: Web application security testing
- **NoScript**: Test CSP enforcement

### Manual Testing Commands

```bash
# Test CSP headers
curl -I http://localhost:8000/bookshelf/

# Test with malicious input
curl "http://localhost:8000/bookshelf/?search=<script>alert('XSS')</script>"
```

## Reporting Issues

If you find security vulnerabilities:

1. **DO NOT** publicly disclose immediately
2. Document the issue with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Potential impact
3. Report to project maintainers
4. Wait for fix before public disclosure

## Summary

After completing all tests, you should verify:

- ✅ SQL injection attempts are blocked
- ✅ Input validation works correctly
- ✅ CSRF tokens are required and validated
- ✅ XSS payloads are escaped
- ✅ CSP headers are present and enforced
- ✅ Authentication and authorization work correctly
- ✅ Security headers are configured properly

All security measures should work together to provide defense in depth against common web application vulnerabilities.

