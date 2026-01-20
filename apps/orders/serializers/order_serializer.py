from rest_framework import serializers
from apps.orders.models.order_model import Order
from .order_item_serializer import OrderItemSerializer



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "total_amount", "payment_status","order_status", "created_at", "items"]
