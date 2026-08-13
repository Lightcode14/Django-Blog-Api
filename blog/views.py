from django.shortcuts import render
from rest_framework import viewsets, generics, status
from.models import Post,Comment,Category
from rest_framework.permissions import (
IsAuthenticatedOrReadOnly,AllowAny, IsAuthenticated
)
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import( 
PostSerializer, Categoryserializer,RegisterSerializer,
CommentSerializer)
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

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response(
            {"message": "Successfully logged out."},
            status=status.HTTP_200_OK
        )