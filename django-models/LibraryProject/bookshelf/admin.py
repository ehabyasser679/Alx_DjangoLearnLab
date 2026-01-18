from django.contrib import admin
from .models import book


@admin.register(book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)
    list_per_page = 10
    list_editable = ('author', 'publication_year')
    ordering = ('title',)
