from django.db import models
from django.conf import settings
from apps.products.models.product_model import Product

User = settings.AUTH_USER_MODEL


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    comment = models.TextField()

    recommend = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]
        indexes = [
        models.Index(fields=['product', '-created_at']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.user}"
