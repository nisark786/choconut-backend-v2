from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.payments.models.payment_model import Payment
from apps.orders.models import Order
from apps.payments.services.razorpay_service import RazorpayService



class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)

        razorpay_order = RazorpayService.create_order(
            amount=order.total_amount,
            receipt=str(order.id)
        )

        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            gateway_order_id=razorpay_order["id"]
        )

        return Response({
            "razorpay_order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": "INR",
            "key": "RAZORPAY_KEY_ID_FROM_FRONTEND_ENV"
        },status=status.HTTP_200_OK)

