from rest_framework import serializers
from apps.products.serializers.product_serializer import ProductSerializer
from apps.cart.models.cart_item_model import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "price_at_added",
            "total_price",
        ]
