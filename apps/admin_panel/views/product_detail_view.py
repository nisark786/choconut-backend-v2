from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.products.models.product_model import Product
from apps.admin_panel.serializers.product_serializer import AdminProductSerializer
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.db import transaction

class AdminProductDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, product_id):
        product = get_object_or_404(Product.objects.select_related("category"), id=product_id)
        serializer = AdminProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = AdminProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(AdminProductSerializer(product).data, status=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({"detail": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
