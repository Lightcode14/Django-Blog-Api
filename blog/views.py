from django.shortcuts import render
from rest_framework import viewsets
from.models import Post,Comment,Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PostSerializer,Categoryserializer,CommentSerializer
from .permissions import IsAuthorOrReadOnly
class PostViewset(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
     

class CategoryViewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=Categoryserializer
class CommentViewset(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]