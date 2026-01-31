
from celery import shared_task
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.accounts.models.user_model import UserModel
from apps.notifications.services import create_user_notification

@shared_task
def send_bulk_notification(title, message, user_ids=None):
    channel_layer = get_channel_layer()
    
   
    if user_ids is None:
        recipients = UserModel.objects.filter(is_active=True,is_staff=False)
    else:
        recipients = UserModel.objects.filter(id__in=user_ids)

    for user in recipients:
        create_user_notification(user, title, message)
        latest_notification = Notification.objects.filter(
            recipient=user,
            recipient_type="USER"
        ).latest("created_at")
        
       
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "send_notification",
                "payload": NotificationSerializer(latest_notification).data
            }
        )