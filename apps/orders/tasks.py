
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task
def cleanup_abandoned_orders():
    from apps.orders.models.order_model import Order
    threshold = timezone.now() - timedelta(hours=24)
    
    abandoned_orders = Order.objects.filter(
        payment_status="PENDING",
        created_at__lt=threshold
    )
    
    count, _ = abandoned_orders.delete()
    return f"Deleted {count} abandoned orders."