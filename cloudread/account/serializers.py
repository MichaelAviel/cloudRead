from django.contrib.auth.models import User
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')

        extra_kwargs = {
            'first_name': {'required':True, 'allow_blank':False },
            'last_name': {'required':True, 'allow_blank':False },
            'username':{'required':True, 'allow_blank':False},
            'email': {'required':True, 'allow_blank':False },
            'password': {'required':True, 'allow_blank':False, 'min_length':8 },
            'password2': {'required':True, 'allow_blank':False, 'min_length':8 },
        }

class UserSerializer(serializers.ModelSerializer):
    wallet_address = serializers.CharField(source='userprofile.wallet_address')
    profile_picture = serializers.CharField(source='userprofile.profile_picture')
    about = serializers.CharField(source = 'userprofile.about')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'profile_picture', 'wallet_address', 'about')