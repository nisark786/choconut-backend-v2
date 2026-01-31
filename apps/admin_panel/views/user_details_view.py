from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Max, Avg
from rest_framework import status
from apps.orders.models.order_model import Order
from apps.accounts.models.user_model import UserModel
from apps.admin_panel.serializers.admin_serializer import AdminUserSerializer
from apps.admin_panel.serializers.order_serializer import AdminOrderSerializer
from apps.admin_panel.permissions.admin_permissions import IsAdminUser


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, id):
        user = get_object_or_404(
            UserModel.objects.only("id", "email", "name"),
            id=id
        )

        orders_qs = (
            Order.objects
            .filter(user_id=user.id)
            .only(
                "id",
                "total_amount",
                "created_at",
                "order_status",
                "payment_status"
            )
            .order_by("-created_at")
        )

        aggregates = orders_qs.aggregate(
            total_orders=Count("id"),
            total_spent=Sum("total_amount"),
            average_order=Avg("total_amount"),
            last_order=Max("created_at"),
        )

        stats = {
            "total_orders": aggregates["total_orders"] or 0,
            "total_spent": aggregates["total_spent"] or 0,
            "average_order": aggregates["average_order"] or 0,
            "last_order": aggregates["last_order"],
        }

        recent_orders = orders_qs[:10]

        return Response({
            "user": AdminUserSerializer(user).data,
            "stats": stats,
            "orders": AdminOrderSerializer(recent_orders, many=True).data
        },status=status.HTTP_200_OK)
