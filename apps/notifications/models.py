from django.db import models
from apps.accounts.models.user_model import UserModel
from apps.products.models.product_model import Product

class Notification(models.Model):
    RECIPIENT_TYPE_CHOICES = (
        ("USER", "User"),
        ("ADMIN", "Admin"),
    )
    recipient_type = models.CharField(
        max_length=10,
        choices=RECIPIENT_TYPE_CHOICES,
        default="USER",
        db_index=True
    )
    recipient = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["recipient_type", "is_read"]),
            models.Index(fields=["recipient", "is_read"]),
        ]



class NotifyMe(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="notify_me")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="notify_requests")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        indexes = [
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"{self.user} → {self.product}"
