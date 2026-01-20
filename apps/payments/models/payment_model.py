from django.db import models
from apps.orders.models.order_model import Order


class Payment(models.Model):
    STATUS_CHOICES = (
        ("INITIATED", "Initiated"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    gateway = models.CharField(max_length=50, default="razorpay")
    gateway_order_id = models.CharField(max_length=255, blank=True, null=True)
    gateway_payment_id = models.CharField(max_length=255, blank=True, null=True)
    gateway_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="INITIATED")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
