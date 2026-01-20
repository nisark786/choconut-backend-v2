from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.products.models.product_model import Product
from apps.products.serializers.product_serializer import ProductSerializer
from apps.products.pagination import ProductPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ProductViewSet(ModelViewSet):
    permission_classes = []
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    queryset = Product.objects.select_related("category").all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = {
        "premium": ["exact"],
        "category__name": ["exact"],
    }

    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @method_decorator(cache_page(60 * 15))
    @action(detail=False, methods=['get'])
    def premium(self, request):
        premium_products = Product.objects.select_related("category").filter(
            premium=True
        ).order_by('-created_at')
        page = self.paginate_queryset(premium_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(premium_products, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)