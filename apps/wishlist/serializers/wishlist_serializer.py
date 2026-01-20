from rest_framework import serializers
from apps.wishlist.models.wishlist_model import Wishlist
from .wishlist_item_serializer import WishlistItemSerializer


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "items",
        ]
