from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.notifications.models import NotifyMe, Notification
from .serializers import NotificationSerializer

MAX_USER_NOTIFICATIONS = 10

def create_user_notification(user, title, message):
    new_notif = Notification.objects.create(
        recipient=user,
        recipient_type="USER",
        title=title,
        message=message
    )

  
    notification_ids = Notification.objects.filter(
        recipient=user,
        recipient_type="USER"
    ).order_by("-created_at").values_list('id', flat=True)

    
    if len(notification_ids) > MAX_USER_NOTIFICATIONS:
        ids_to_delete = notification_ids[MAX_USER_NOTIFICATIONS:]
        Notification.objects.filter(id__in=list(ids_to_delete)).delete()
    
    return new_notif


def notify_users_stock_available(product):
    channel_layer = get_channel_layer()

    notify_entries = NotifyMe.objects.filter(
        product=product
    ).select_related("user")

    for entry in notify_entries:
        create_user_notification(
            user=entry.user,
            title="Stock Available",
            message=f"{product.name} is back in stock. Buy now!"
        )
        latest_notification = Notification.objects.filter(
            recipient=entry.user,
            recipient_type="USER"
        ).latest("created_at")

        payload = NotificationSerializer(latest_notification).data
        payload["product_id"] = product.id
       
        async_to_sync(channel_layer.group_send)(
            f"user_{entry.user.id}",
            {
                "type": "send_notification",
                "payload": payload
            }
        )

        entry.delete()
