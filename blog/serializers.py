from rest_framework import serializers
from .models import Like, Post,Category,Comment
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'
        read_only_fields=["author"]

class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
            model=Like
            fields='__all__'


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','email','password']
        extra_kwargs={
            'password':{'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token