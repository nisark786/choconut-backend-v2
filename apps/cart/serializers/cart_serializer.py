from rest_framework import serializers
from apps.cart.models.cart_model import Cart
from .cart_item_serializer import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    cart_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "cart_total",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['cart_total'] = getattr(instance, 'db_total', 0) or 0
        return data
