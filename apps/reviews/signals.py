from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.reviews.models.review_model import Review


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    stats = product.reviews.aggregate(
        avg=Avg("rating"),
        count=Count("id")
    )

    product.rating_avg = round(stats["avg"] or 0, 1)
    product.rating_count = stats["count"]
    product.save(update_fields=["rating_avg", "rating_count"])
