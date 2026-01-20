from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.orders.models import Order
from apps.orders.serializers.order_serializer import OrderSerializer


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related('items__product')
            .order_by("-created_at")
        )

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
