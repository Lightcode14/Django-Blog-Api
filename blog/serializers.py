from rest_framework import serializers
from .models import Like, Post,Category,Comment
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Category
        fields = ['id', 'name', 'slug']





class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model=Comment
        fields='__all__'
    def validate_body(self, value):
     if len(value.strip()) < 3:
        raise serializers.ValidationError(
            "Comment must be at least 3 characters long."
        )
     return value
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
            model=Like
            fields='__all__'
    def validate(self, data):
        user = self.context['request'].user
        post = data.get('post')

        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError(
                "You have already liked this post."
            )

        return data


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



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(source='comment_set', many=True, read_only=True)
    class Meta:
        model=Post
        fields='__all__'
    def validate_title(self, value):
     if len(value) < 5:
        raise serializers.ValidationError(
            "Title must be at least 5 characters long."
        )
     return value
    
    def validate(self, data):
     if data.get('published') and not data.get('content'):
        raise serializers.ValidationError(
            "A post must have content before it can be published."
        )

     return data