from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from requests import get
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .validators import validate_file_extension, validate_profile_image
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg, Min, Max, Count
from .models import Book
from .filters import BooksFilter
# Create your views here.


@api_view(['GET'])
def getAllBooks(request):

    filter_set = BooksFilter(request.GET, queryset=Book.objects.all().order_by('id'))

    count = filter_set.qs.count()

    results_per_page = 20
    paginator = PageNumberPagination()
    paginator.page_size = results_per_page
    queryset = paginator.paginate_queryset(filter_set.qs, request)
    serializer = BookSerializer(queryset, many=True)
    context = {
        'count':count,
        'results_per_page':results_per_page,
        'books': serializer.data,
    }
    return Response(context)

@api_view(['GET'])
def getBook(request, address):

    book = get_object_or_404(Book, book_address=address)
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addBook(request):
    request.data['author'] = request.user
    data = request.data
    # **data is essentially the spread operator that spreads all the data in the create function for the Job fields. 

    book = Book.objects.create(**data)

    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def updateBook(request, address):

    book = get_object_or_404(Book, book_address=address)

    if book.author != request.user:
        return Response({
            'message':'Forbidden Access, you are not the owner of this posting'
        }, status= status.HTTP_403_FORBIDDEN)

    book.title = request.data['title']
    book.description = request.data['description']
    book.description_short = request.data['description_short']
    book.file = request.FILES['file']
    book.book_genre = request.data['book_genre']
    book.book_category = request.data['book_category']
    book.cover_image = request.FILES['cover_image']

    is_valid_file = validate_file_extension(book.file.name)

    if not is_valid_file:
        return Response({
            'error':'At this moment you can only upload a PDF'
        },status=status.HTTP_400_BAD_REQUEST)

    is_valid_image = validate_profile_image(book.cover_image.name)

    if not is_valid_image:
        return Response({
            'error':'Only Image types are jpg, jpeg or png.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if book.file == '':
        return Response({
            'error':'Please upload your book'
        })

    book.save()

    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteJob(request, address):
    book = get_object_or_404(Book, book_address=address)
    if book.author != request.user:
        return Response({
            'message':'Forbidden Access, you are not the owner of this posting'
        }, status= status.HTTP_403_FORBIDDEN)

    book.delete()

    return Response({ 'message': 'Book is Deleted.' }, status=status.HTTP_200_OK)



@api_view(['GET'])
def getTopicStats(request, topic):
    # Matches the title that contains the topic.
    args = { 'title__icontains': topic }
    books = Book.objects.filter(**args)

    if len(books) == 0:
        return Response({ 'message': 'Not stats found for {topic}'.format(topic=topic) })

    
    stats = books.aggregate(
        total_category = Count('book_category'),
        total_genre = Count('book_genre'),
    )

    return Response(stats)

