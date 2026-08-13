from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewset,CategoryViewset,CommentViewset


router=DefaultRouter()

router.register("posts",PostViewset)
router.register("comments",CommentViewset)
router.register("categories",CategoryViewset)


urlpatterns=[
    path("", include(router.urls))
]