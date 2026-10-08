from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
 LikeViewset, PostViewset,CategoryViewset,CommentViewset,RegisterView,LogoutView,MyTokenObtainPairView   
) 
from rest_framework_simplejwt.views import(
 TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

router=DefaultRouter()

router.register("posts",PostViewset)
router.register("comments",CommentViewset)
router.register("categories",CategoryViewset)
router.register("likes",LikeViewset)


urlpatterns=[
    path("", include(router.urls)),
    path("register/",RegisterView.as_view(), name="register"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("token/refresh/" ,TokenRefreshView.as_view(),name="token-refresh"),
    path("token/" ,MyTokenObtainPairView.as_view(),name="token-obtain"),
    path("schema/" ,SpectacularAPIView.as_view(),name="schema"),
    path("docs/" ,SpectacularSwaggerView.as_view(url_name='schema'),name="swagger-ui"),
    
]