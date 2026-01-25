from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from apps.notifications.models import NotifyMe
from apps.products.models.product_model import Product
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from .tasks import send_bulk_notification

class AdminNotificationListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient_type="ADMIN"
        ).order_by("-created_at")[:20]

        unread_count = notifications.filter(is_read=False).count()

        return Response({
            "notifications": NotificationSerializer(notifications, many=True).data,
            "unread_count": unread_count
        })



class AdminBroadcastView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        title = request.data.get("title")
        message = request.data.get("message")
        target_user_id = request.data.get("user_id") # Optional
        user_ids = request.data.get("user_ids", [])

        if not title or not message:
            return Response({"error": "Title and message required"}, status=400)

        send_bulk_notification.delay(title, message, user_ids if user_ids else None)

        return Response({"detail": "Broadcast process initiated."})


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch latest 10 notifications for the logged-in user
        notifications = Notification.objects.filter(
            recipient=request.user,
            recipient_type="USER"
        ).order_by('-created_at')[:10]
        
        serializer = NotificationSerializer(notifications, many=True)
        
        # We also send the unread count in the same request for convenience
        unread_count = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).count()
        
        return Response({
            "notifications": serializer.data,
            "unread_count": unread_count
        }, status=status.HTTP_200_OK)

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {"detail": "Notification not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        return Response(
            {"message": "Notification marked as read"},
            status=status.HTTP_200_OK
        )
    


class NotifyMeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notify_entries = NotifyMe.objects.filter(user=request.user).select_related("product")
        product_ids = [entry.product.id for entry in notify_entries]

        return Response({
            "items": [{"product": {"id": entry.product.id, "name": entry.product.name}} for entry in notify_entries],
            "product_ids": product_ids
        }, status=status.HTTP_200_OK)


class AddNotifyMeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"detail": "Product not found"}, status=404)

        if product.stock > 0:
            return Response(
                {"detail": "Product is already in stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        NotifyMe.objects.get_or_create(
            user=request.user,
            product=product
        )

        return Response(
            {"detail": "You will be notified when product is back in stock"},
            status=status.HTTP_201_CREATED
        )
    
class RemoveNotifyMeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        NotifyMe.objects.filter(
            user=request.user,
            product_id=product_id
        ).delete()

        return Response(
            {"detail": "Removed from notify me"},
            status=status.HTTP_200_OK
        )
