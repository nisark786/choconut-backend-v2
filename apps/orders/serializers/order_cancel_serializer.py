
from rest_framework import serializers
from apps.orders.models import Order


class OrderCancelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = []  

    def validate(self, attrs):
        order = self.instance

        if order.order_status == "DELIVERED":
            raise serializers.ValidationError(
                "Delivered orders cannot be cancelled."
            )

        if order.order_status == "CANCELLED":
            raise serializers.ValidationError(
                "Order is already cancelled."
            )

        return attrs

    def save(self, **kwargs):
        order = self.instance
        order.order_status = "CANCELLED"
        order.save(update_fields=["order_status"])
        return order
