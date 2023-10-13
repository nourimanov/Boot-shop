from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import ProductClassViewSet, CategoryClassViewSet, ProductImageViewSet, ProductColorViewSet, \
    IsActiveViewSet, UserView, UserActiveView, ProductShopModelViewSet, ContactListCreateAPIView

router = DefaultRouter()
router.register('products', ProductClassViewSet, basename='products')
router.register('categories', CategoryClassViewSet, basename='categories')
router.register('images', ProductImageViewSet, basename='images')
router.register('colors', ProductColorViewSet, basename='colors')
router.register('users', UserView, 'user')
router.register("shop", ProductShopModelViewSet, basename="product_shop")


urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pk>/active/', IsActiveViewSet.as_view(), name="product_active"),
    path('contact/', ContactListCreateAPIView.as_view(), name="contact"),
    path('users/<int:pk>/active/', UserActiveView.as_view(), name="active_user")
]
