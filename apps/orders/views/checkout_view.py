from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers.order_serializer import OrderSerializer
from ..services.order_service import OrderService


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            order = OrderService.create_order_from_cart(request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
