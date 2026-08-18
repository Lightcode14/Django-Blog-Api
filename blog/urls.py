from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
 PostViewset,CategoryViewset,CommentViewset,RegisterView,LogoutView,MyTokenObtainPairView   
) 
from rest_framework_simplejwt.views import(
 TokenObtainPairView,
 TokenRefreshView,
)

router=DefaultRouter()

router.register("posts",PostViewset)
router.register("comments",CommentViewset)
router.register("categories",CategoryViewset)


urlpatterns=[
    path("", include(router.urls)),
    path("register/",RegisterView.as_view(), name="register"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("token/" ,MyTokenObtainPairView.as_view(),name="token-obtain"),
    path("token/refresh/" ,TokenRefreshView.as_view(),name="token-refresh"),
    
]