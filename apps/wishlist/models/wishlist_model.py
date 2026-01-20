from django.db import models
from apps.accounts.models.user_model import UserModel


class Wishlist(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Wishlist"
