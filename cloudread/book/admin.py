from django.contrib import admin
from .models import Book
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'book_genre', 'book_category', 'created_at')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'author', 'book_genre', 'company', 'book_category')