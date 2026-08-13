from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
 PostViewset,CategoryViewset,CommentViewset,RegisterView,LogoutView   
) 


router=DefaultRouter()

router.register("posts",PostViewset)
router.register("comments",CommentViewset)
router.register("categories",CategoryViewset)


urlpatterns=[
    path("", include(router.urls)),
    path("register/",RegisterView.as_view(), name="register"),
    path("logout/",LogoutView.as_view(), name="logout"),

]