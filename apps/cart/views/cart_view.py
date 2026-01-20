from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, F
from apps.cart.serializers.cart_serializer import CartSerializer
from apps.cart.services.cart_service import CartService
from apps.cart.models.cart_model import Cart


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_query = Cart.objects.filter(user=request.user).prefetch_related(
            "items__product"
        ).annotate(
            db_total=Sum(F('items__quantity') * F('items__price_at_added'))
        ).first()

        if not cart_query:
            cart_query = CartService.get_or_create_cart(request.user)

        serializer = CartSerializer(cart_query)
        return Response(serializer.data, status=status.HTTP_200_OK)
