from rest_framework import serializers
from .models import Post,Category,Comment
from django.contrib.auth.models import User

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