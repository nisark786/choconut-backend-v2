from rest_framework import serializers
from apps.orders.models.order_model import Order
from apps.orders.models.order_item_model import OrderItem
from apps.orders.models.order_address_model import OrderAddress

class AdminOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "product_name", "quantity", "price"]

class AdminOrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        exclude = ("order",)

class AdminOrderSerializer(serializers.ModelSerializer):
    items = AdminOrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    address = AdminOrderAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user_name",
            "user_email",
            "total_amount",
            "payment_status",
            "order_status",
            "created_at",
            "items",
            "address",
        ]

class AdminOrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order_status"]

    def validate_order_status(self, value):
        valid_statuses = [status for status, _ in Order.ORDER_STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid order status.")
        return value
