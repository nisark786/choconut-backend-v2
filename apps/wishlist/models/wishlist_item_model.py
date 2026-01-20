from django.db import models
from .wishlist_model import Wishlist
from apps.products.models.product_model import Product


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("wishlist", "product")
        indexes = [
            models.Index(fields=['wishlist', 'product']),
        ]

    def __str__(self):
        return f"{self.product.name}"
