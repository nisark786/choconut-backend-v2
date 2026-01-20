from django.db import models
from .cart_model import Cart
from apps.products.models.product_model import Product




class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_added = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        unique_together = ("cart", "product")
        indexes = [
            models.Index(fields=["cart", "product"]),
        ]

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price_at_added