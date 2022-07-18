from .models import Book
from django_filters import rest_framework as filters



class BooksFilter(filters.FilterSet):
    # gte is greater than ir equal to
    # lte is less than or equal to. 
    keyword = filters.CharFilter(field_name='title', lookup_expr='icontains')
    location = filters.CharFilter(field_name='address', lookup_expr='icontains')
    author = filters.CharFilter(field_name="author", lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ('book_genre', 'book_category', 'keyword', 'author')