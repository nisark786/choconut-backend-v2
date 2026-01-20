from django.db import models
from .category_model import Category




class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    image = models.URLField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    premium = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    rating_avg = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['premium', '-created_at']),
            models.Index(fields=['category', 'price']),
        ]

    def __str__(self):
        return self.name