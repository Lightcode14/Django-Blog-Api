from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import serializers, viewsets, generics, status
from.models import Like, Post,Comment,Category
from rest_framework.permissions import (
IsAuthenticatedOrReadOnly,AllowAny, IsAuthenticated

)
from drf_spectacular.utils import extend_schema
from django.db.models import Q
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

    def get_queryset(self):
        user = self.request.user

        # Staff can access all posts.
        if user.is_authenticated and user.is_staff:
            return Post.objects.all()

        # Authenticated users can see published posts
        # and their own unpublished posts.
        if user.is_authenticated:
            return Post.objects.filter(
                Q(published=True) | Q(author=user)
            )

        # Anonymous users can only see published posts.
        return Post.objects.filter(published=True)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
     

class CategoryViewset(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    filter_backend=[SearchFilter]
    search_fields=['name']

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if "post" in self.request.data:
            requested_post_id = self.request.data.get("post")

            if str(requested_post_id) != str(serializer.instance.post_id):
                raise serializers.ValidationError({
                    "post": "You cannot change the post of an existing comment."
                })

        serializer.save()
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


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=inline_serializer(
            name="LogoutRequest",
            fields={
                "refresh": serializers.CharField(),
            },
        ),
        responses={
            205: None,
            400: inline_serializer(
                name="LogoutError",
                fields={
                    "error": serializers.CharField(),
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )

        except TokenError:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer