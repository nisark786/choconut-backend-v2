from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.payments.models.payment_model import Payment
from apps.payments.services.razorpay_service import RazorpayService
from apps.payments.serializers.payment_verify_serializer import PaymentVerifySerializer
from apps.cart.models.cart_item_model import CartItem
from django.db import transaction




class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = PaymentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            RazorpayService.verify_signature(data)
        except Exception:
            return Response({"detail": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.select_for_update().get(gateway_order_id=data["razorpay_order_id"])
        payment.gateway_payment_id = data["razorpay_payment_id"]
        payment.gateway_signature = data["razorpay_signature"]
        payment.status = "SUCCESS"
        payment.save()

        order = payment.order
        order.payment_status = "PAID"
        order.save()

        CartItem.objects.filter(cart__user=request.user).delete()

        return Response({"detail": "Payment successful"}, status=status.HTTP_200_OK)