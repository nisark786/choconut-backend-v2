from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.products.models.product_model import Product
from apps.admin_panel.serializers.product_serializer import AdminProductSerializer
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from django.db import transaction
from django.core.paginator import Paginator

class AdminProductListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        products = Product.objects.select_related("category").filter()
        paginator = Paginator(products, 12) 
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        serializer = AdminProductSerializer(page_obj, many=True)
        return Response({
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "results": serializer.data,
        })

    @transaction.atomic
    def post(self, request):
        serializer = AdminProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(AdminProductSerializer(product).data, status=status.HTTP_201_CREATED)
