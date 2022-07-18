from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    class Meta:
        model=Book
        fields = ('title', 'description', 'description_short', 'book_address', 'book_genre', 'book_category', 'secret_access_code', 'author', 'created_at')
