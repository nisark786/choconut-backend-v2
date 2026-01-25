from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from apps.orders.models.order_model import Order
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.notifications.services import create_user_notification



@receiver(post_save, sender=Order)
def order_notification_handler(sender, instance, created, **kwargs):
    if not created:
        return

    channel_layer = get_channel_layer()

    # 1️⃣ USER notification
    create_user_notification(
        user=instance.user,
        title="Order Placed",
        message=f"Your order #{instance.id} has been placed successfully!"
    )
    latest = Notification.objects.filter(
        recipient=instance.user,
        recipient_type="USER"
    ).latest("created_at")

    async_to_sync(channel_layer.group_send)(
        f"user_{instance.user.id}",
        {
            "type": "send_notification",
            "payload": NotificationSerializer(latest).data
        }
    )

    admin_notif = Notification.objects.create(
        recipient_type="ADMIN",
        title="New Order Received",
        message=f"Order #{instance.id} placed by {instance.user.email}"
    )

    async_to_sync(channel_layer.group_send)(
        "admins",
        {
            "type": "send_notification",
            "payload": NotificationSerializer(admin_notif).data
        }
    )





@receiver(pre_save, sender=Order)
def store_old_order_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Order.objects.get(pk=instance.pk)
            instance._old_status = old.order_status
        except Order.DoesNotExist:
            instance._old_status = None



@receiver(post_save, sender=Order)
def notify_user_on_status_change(sender, instance, created, **kwargs):
    if created:
        return  

    old_status = getattr(instance, "_old_status", None)
    new_status = instance.order_status

    if old_status == new_status:
        return  # No change → no notification

    STATUS_MESSAGES = {
        "PROCESSING": "Your order is being processed",
        "SHIPPED": "Your order has been shipped",
        "DELIVERED": "Your order has been delivered",
        "CANCELLED": "Your order has been cancelled",
    }

    title = f"{STATUS_MESSAGES.get(new_status, new_status)}"
    message = f"Order #{instance.id}: Is Ready Now"

    # 1️⃣ Save notification
    create_user_notification(
        user=instance.user,
        title=title,
        message=message
    )
    notification = Notification.objects.filter(
        recipient=instance.user,
        recipient_type="USER"
    ).latest("created_at")

    # 2️⃣ Push via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{instance.user.id}",
        {
            "type": "send_notification",
            "payload": NotificationSerializer(notification).data
        },
    )
