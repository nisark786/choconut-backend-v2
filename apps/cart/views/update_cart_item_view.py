from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.cart.services.cart_service import CartService
from apps.cart.models.cart_model import Cart
from apps.cart.serializers.cart_serializer import CartSerializer
from django.db.models import Sum,F



class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity"))

        CartService.update_quantity(
            request.user,
            product_id,
            quantity
        )
        cart = Cart.objects.filter(user=request.user).annotate(
            db_total=Sum(F('items__quantity') * F('items__price_at_added'))
        ).first()
        serializer = CartSerializer(cart)

        return Response(serializer.data,status=status.HTTP_200_OK)
