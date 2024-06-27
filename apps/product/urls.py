from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
    ProductImageViewSet,
    TraderViewSet,
    WishlistViewSet,
    RankViewSet,
    CommentViewSet,

)


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('', ProductViewSet)
router.register(r'(?P<pid>[0-9]+)/images', ProductImageViewSet)
router.register('trade', TraderViewSet)
router.register('wishlist', WishlistViewSet)
router.register(r'(?P<pid>[0-9]+)/ranks', RankViewSet)
router.register(r'(?P<pid>[0-9]+)/comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]