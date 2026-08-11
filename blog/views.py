from django.shortcuts import render
from rest_framework import viewsets
from.models import Post,Comment,Category
from .serializers import PostSerializer,Categoryserializer,CommentSerializer
class PostViewset(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

class CategoryViewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=Categoryserializer
class CommentViewset(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer