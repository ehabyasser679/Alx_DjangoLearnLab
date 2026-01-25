from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import book, CustomUser


@admin.register(book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)
    list_per_page = 10
    list_editable = ('author', 'publication_year')
    ordering = ('title',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    list_per_page = 10
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Fields', {'fields': ('phone_number', 'bio', 'date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Fields', {'fields': ('phone_number', 'bio', 'date_of_birth', 'profile_photo')}),
    )

