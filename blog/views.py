from django.shortcuts import render
from rest_framework import viewsets, generics, status
from.models import Like, Post,Comment,Category
from rest_framework.permissions import (
IsAuthenticatedOrReadOnly,AllowAny, IsAuthenticated
)
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import( 
LikeSerializer, PostSerializer, Categoryserializer,RegisterSerializer,
CommentSerializer, MyTokenObtainPairSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAuthorOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
class PostViewset(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAuthorOrReadOnly]
    filter_backend=[SearchFilter]
    search_fields=['title','content']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
     

class CategoryViewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=Categoryserializer
    filter_backend=[SearchFilter]
    search_fields=['name']

class CommentViewset(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
            return serializer.save(user=self.request.user)

class LikeViewset(viewsets.ModelViewSet):
    serializer_class=LikeSerializer
    queryset=Like.objects.all()
      ##  def get_queryset(self):
        ##return Like.objects.all()
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
         try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )

         except Exception:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer