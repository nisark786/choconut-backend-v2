from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.orders.models.order_model import Order
from apps.admin_panel.serializers.order_serializer import (
    AdminOrderSerializer,
    AdminOrderStatusUpdateSerializer,
)
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.cache import cache
from apps.admin_panel.paginations import AdminPagination
from django.db.models import Q
from apps.admin_panel.utils.cache_keys import clear_admin_order_stats_cache




def get_order_stats():
    cache_key = "admin_order_stats"
    stats = cache.get(cache_key)

    if not stats:
        stats = dict(
            Order.objects.values("order_status")
            .annotate(count=Count("id"))
            .values_list("order_status", "count")
        )
        cache.set(cache_key, stats, 300)

    return stats


class AdminOrderListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        search = request.query_params.get("search")
        status_filter = request.query_params.get("status")

        queryset = (
            Order.objects
            .select_related("user")
            .prefetch_related("items__product", "address")
            .order_by("-created_at")
        )

      
        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) |
                Q(user__name__icontains=search) |
                Q(user__email__icontains=search)
            )

        if status_filter and status_filter != "all":
            queryset = queryset.filter(order_status=status_filter)

        paginator = AdminPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = AdminOrderSerializer(page, many=True)

        return paginator.get_paginated_response({
            "results": serializer.data,
            "stats": get_order_stats(),
        })


class AdminOrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = AdminOrderStatusUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        transaction.on_commit(clear_admin_order_stats_cache)

        return Response({"detail": "Order status updated"},status=status.HTTP_200_OK)