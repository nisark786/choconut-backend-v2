from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from apps.products.models.product_model import Product
from apps.admin_panel.serializers.product_serializer import AdminProductSerializer
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from apps.admin_panel.paginations import AdminPagination
from rest_framework import status
from apps.admin_panel.serializers.product_serializer import (
    AdminProductCreateSerializer
)


class AdminProductListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        search = request.query_params.get("search")
        category = request.query_params.get("category")
        premium = request.query_params.get("premium")
        stock = request.query_params.get("stock")

        base_queryset = Product.objects.select_related("category")
        stats = {
            "total": base_queryset.count(),
            "low_stock": base_queryset.filter(stock__gt=0, stock__lte=10).count(),
            "out_of_stock": base_queryset.filter(stock__lte=0).count(),
            "categories": base_queryset.values("category").distinct().count(),
        }

        queryset = base_queryset.only(
            "id",
            "name",
            "price",
            "image",
            "premium",
            "stock",
            "description",
            "category__name",
        ).order_by("-id")

      
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(category__name=category)

        if premium in ["true", "false"]:
            queryset = queryset.filter(premium=premium == "true")

        if stock == "out":
            queryset = queryset.filter(stock__lte=0)
        elif stock == "low":
            queryset = queryset.filter(stock__lte=5)

      
        paginator = AdminPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = AdminProductSerializer(page, many=True)

        return paginator.get_paginated_response({
            "products": serializer.data,
            "stats": stats,
        })
    
    def post(self, request):
        serializer = AdminProductCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        return Response(
            {
                "id": product.id,
                "message": "Product created successfully"
            },
            status=status.HTTP_201_CREATED
        )
