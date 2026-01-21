from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.products.models.product_model import Product
from apps.admin_panel.serializers.product_serializer import AdminProductSerializer,AdminProductUpdateSerializer
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.db import transaction

class AdminProductDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, product_id):
        product = get_object_or_404(
            Product.objects.select_related("category"),
            id=product_id
        )
        serializer = AdminProductSerializer(product)
        return Response(serializer.data)

    @transaction.atomic
    def patch(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = AdminProductUpdateSerializer(
            product,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(AdminProductSerializer(product).data)

    @transaction.atomic
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
