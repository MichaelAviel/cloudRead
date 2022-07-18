from . import views
from django.urls import path

urlpatterns = [
    path('books/', views.getAllBooks, name='books'),
    path('books/<str:address>/', views.getBook, name='book'),
    path('books/add/', views.addBook, name='add_book'),
    path('books/<str:address>/update/', views.updateBook, name='update_book'),
    path('stats/<str:topic>/', views.getTopicStats, name='get_topic_stats'),
]
