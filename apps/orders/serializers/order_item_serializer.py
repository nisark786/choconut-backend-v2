from rest_framework import serializers
from apps.orders.models.order_model import Order
from apps.orders.models.order_item_model import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "product_name", "quantity", "price"]


