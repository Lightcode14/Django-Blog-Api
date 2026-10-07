from django.shortcuts import render
from rest_framework import viewsets, generics, status
from.models import Like, Post,Comment,Category
from rest_framework.permissions import (
IsAuthenticatedOrReadOnly,AllowAny, IsAuthenticated

)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import( 
LikeSerializer, PostSerializer, CategorySerializer,RegisterSerializer,
CommentSerializer, MyTokenObtainPairSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAuthorOrReadOnly,IsLikeOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework_simplejwt.tokens import RefreshToken


class PostViewset(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAuthorOrReadOnly,IsAuthenticatedOrReadOnly]
    filter_backend=[SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields=['created_at','updated_at','title']
    search_fields=['title','content']
    filterset_fields=['categories','published']
    parser_classes=[MultiPartParser,FormParser]
    ordering=['created_at']
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
     

class CategoryViewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    filter_backend=[SearchFilter]
    search_fields=['name']

class CommentViewset(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]
    def perform_create(self, serializer):
           serializer.save(author=self.request.user)

class LikeViewset(viewsets.ModelViewSet):
    serializer_class=LikeSerializer
    queryset=Like.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly,IsLikeOwnerOrReadOnly]
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