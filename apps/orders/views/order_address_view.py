# apps/orders/views/order_address_view.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.orders.models.order_model import Order
from apps.orders.models.order_address_model import OrderAddress
from apps.orders.serializers.order_address_serializer import OrderAddressSerializer



class OrderAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = OrderAddress.objects.filter(order__user=request.user)
        serializer = OrderAddressSerializer(addresses, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user, payment_status="PENDING")
        except Order.DoesNotExist:
            return Response({"detail": "Invalid order"}, status=status.HTTP_400_BAD_REQUEST)

        address_id = request.data.get("address_id")

        if address_id:
            # CASE: Existing address
            try:
                address = OrderAddress.objects.get(id=address_id, order__user=request.user)
            except OrderAddress.DoesNotExist:
                return Response({"detail": "Invalid address"}, status=status.HTTP_400_BAD_REQUEST)
            
            order.address = address
            order.save()
            return Response({"detail": "Address selected"}, status=status.HTTP_200_OK)

        else:
            serializer = OrderAddressSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            address = serializer.save(order=order)

            order.address = address
            order.save()

            return Response(
                OrderAddressSerializer(address).data,
                status=status.HTTP_201_CREATED
            )

