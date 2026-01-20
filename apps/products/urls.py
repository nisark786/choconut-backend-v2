# apps/products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.product_view import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
