
from rest_framework import serializers
from apps.orders.models.order_address_model import OrderAddress

class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        exclude = ("order",)
