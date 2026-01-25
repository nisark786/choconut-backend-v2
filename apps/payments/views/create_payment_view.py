from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.payments.models.payment_model import Payment
from apps.orders.models import Order
from apps.payments.services.razorpay_service import RazorpayService
from apps.cart.models.cart_model import Cart


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists():
                return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found"}, status=status.HTTP_400_BAD_REQUEST)
        subtotal = cart.total_price  # Assuming your Cart model has a total_price property
        shipping = 0 if subtotal > 499 else 49
        total_amount = subtotal + shipping
        razorpay_order = RazorpayService.create_order(
            amount=total_amount,
            receipt=f"cart_{cart.id}"
        )
        Payment.objects.create(
            user=request.user,
            amount=total_amount,
            gateway_order_id=razorpay_order["id"],
            status="PENDING" 
        )
        

        return Response({
            "razorpay_order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": "INR",
        },status=status.HTTP_200_OK)

