"""
Forms for the bookshelf application.

This module contains form classes with input validation and sanitization
to ensure secure data handling and prevent SQL injection attacks.
"""

from django import forms
from django.forms import ModelForm
from .models import book


# Form for book model with input validation
# Security: Using ModelForm ensures automatic validation and prevents SQL injection
# Django ORM automatically parameterizes queries, preventing SQL injection attacks
class BookForm(ModelForm):
    """
    Form for creating and editing book entries.
    
    Security features:
    - Automatic input validation via Django ModelForm
    - Custom clean methods for additional validation
    - Input sanitization (whitespace stripping, length limits)
    - Type validation for publication year
    """
    
    class Meta:
        model = book
        fields = ['title', 'author', 'publication_year']
    
    def clean_title(self):
        """
        Validate and sanitize title input.
        
        Security: Strips whitespace and enforces length limits to prevent
        buffer overflow attacks and ensure data integrity.
        """
        title = self.cleaned_data.get('title')
        if title:
            # Strip whitespace and limit length
            title = title.strip()[:200]  # Max length matches model field
            if not title:
                raise forms.ValidationError("Title cannot be empty.")
        return title
    
    def clean_author(self):
        """
        Validate and sanitize author input.
        
        Security: Strips whitespace and enforces length limits to prevent
        buffer overflow attacks and ensure data integrity.
        """
        author = self.cleaned_data.get('author')
        if author:
            # Strip whitespace and limit length
            author = author.strip()[:100]  # Max length matches model field
            if not author:
                raise forms.ValidationError("Author cannot be empty.")
        return author
    
    def clean_publication_year(self):
        """
        Validate publication year to prevent invalid dates.
        
        Security: Ensures year is within reasonable range to prevent
        invalid data entry and potential issues with date handling.
        """
        year = self.cleaned_data.get('publication_year')
        if year:
            # Ensure year is reasonable (between 1000 and current year + 1)
            from datetime import datetime
            current_year = datetime.now().year
            if year < 1000 or year > current_year + 1:
                raise forms.ValidationError(
                    f"Publication year must be between 1000 and {current_year + 1}."
                )
        return year

