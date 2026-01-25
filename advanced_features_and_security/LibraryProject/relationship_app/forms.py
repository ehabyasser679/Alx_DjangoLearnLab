from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form that uses the custom user model"""
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

