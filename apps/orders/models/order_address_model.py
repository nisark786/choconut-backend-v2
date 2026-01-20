# apps/orders/models/order_address_model.py
from django.db import models
from .order_model import Order

class OrderAddress(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="address"
    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"Address for Order #{self.order.id}"
