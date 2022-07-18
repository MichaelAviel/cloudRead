from django.contrib.auth.hashers import make_password
from requests import get
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from book.validators import validate_file_extension, validate_profile_image
from rest_framework.response import Response
from .serializers import SignUpSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import mixins, generics, viewsets, status

# Create your views here.



@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)
    print(user)

    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists():
            if data['password'] == data['password2']:
                user = User.objects.create(
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    username = data['username'],
                    email = data['email'],
                    password = make_password(data['password'])
                )
                return Response({
                    'message':'You Have been Registered'},
                    status = status.HTTP_200_OK)
            else:
                return Response({
                    'error':'Your Passwords Do not match please try again'},
                    status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                    'error':'User already Exist'},
                    status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):

    user = request.user
    serializer = UserSerializer(user)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):

    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['username']
    user.email = data['email']
    user.userprofile.about = data['about']
    user.userprofile.wallet_address = data['wallet_address']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def upload_profile_image(request):

    user = request.user
    profile_image = request.FILES['profile_picture']

    is_valid_image = validate_profile_image(profile_image.name)

    if not is_valid_image:
        return Response({
            'error':'Only Image types are jpg, jpeg or png.'
        })

    if profile_image == '':
        return Response({
            'error':'Please upload your profile picture'
        })

    user.userprofile.profile_picture = profile_image
    user.userprofile.save()


    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
