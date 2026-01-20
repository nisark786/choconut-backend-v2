from rest_framework import serializers
from apps.wishlist.models.wishlist_item_model import WishlistItem
from apps.products.serializers.product_serializer import ProductSerializer


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product",
            "added_at",
        ]
