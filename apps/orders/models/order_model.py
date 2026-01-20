from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    )

    ORDER_STATUS_CHOICES = (
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="PROCESSING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]


    def __str__(self):
        return f"Order #{self.id} - {self.order_status}"


