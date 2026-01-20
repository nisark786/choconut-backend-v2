from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.orders.models import Order
from apps.orders.serializers.order_cancel_serializer import OrderCancelSerializer


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

        serializer = OrderCancelSerializer(instance=order,data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Order cancelled successfully"},
            status=status.HTTP_200_OK
        )
