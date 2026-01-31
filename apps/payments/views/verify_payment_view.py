from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.payments.models.payment_model import Payment
from apps.payments.services.razorpay_service import RazorpayService
from apps.payments.serializers.payment_verify_serializer import PaymentVerifySerializer
from apps.orders.models.order_model import Order
from apps.orders.models.order_address_model import OrderAddress
from apps.orders.services.order_service import OrderService
from apps.cart.models.cart_item_model import CartItem

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

     
        payment = get_object_or_404(Payment, gateway_order_id=data["razorpay_order_id"])

      
        try:
           
            order = OrderService.create_order_from_cart(request.user)
            
            address_id = request.data.get("address_id")
            new_address_data = request.data.get("new_address")

            if address_id:
                
                address = OrderAddress.objects.filter(id=address_id).first()
                if not address:
                    return Response({"detail": "Invalid Address ID"}, status=status.HTTP_400_BAD_REQUEST)
                order.address = address
            elif new_address_data:
                new_address_data.pop('user', None)
               
                address = OrderAddress.objects.create(order=order, **new_address_data)
                order.address = address
            else:
                return Response({"detail": "Address is required"}, status=status.HTTP_400_BAD_REQUEST)

           
            order.payment_status = "PAID"
            order.save()

            payment.order = order  
            payment.gateway_payment_id = data["razorpay_payment_id"]
            payment.gateway_signature = data["razorpay_signature"]
            payment.status = "SUCCESS"
            payment.save()

        
            CartItem.objects.filter(cart__user=request.user).delete()

            return Response({
                "detail": "Order placed successfully",
                "order_id": order.id
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)