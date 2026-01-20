from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils.timezone import now
from django.core.cache import cache

from apps.accounts.models.user_model import UserModel
from apps.admin_panel.serializers.admin_serializer import AdminUserSerializer
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from apps.admin_panel.paginations import AdminUserPagination


def get_user_stats():
    cache_key = "admin_user_stats"
    stats = cache.get(cache_key)

    if not stats:
        stats = {
            "total": UserModel.objects.count(),
            "active": UserModel.objects.filter(
                is_active=True, is_blocked=False
            ).count(),
            "blocked": UserModel.objects.filter(is_blocked=True).count(),
            "not_verified": UserModel.objects.filter(is_verified=False).count(),
            "new_this_month": UserModel.objects.filter(
                date_joined__month=now().month,
                date_joined__year=now().year
            ).count(),
        }
        cache.set(cache_key, stats, timeout=300)  # cache for 5 minutes

    return stats



class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        search = request.query_params.get("search")
        status_filter = request.query_params.get("status")
        include_orders = request.query_params.get("include_orders") == "true"

        # Base queryset (minimized fields)
        queryset = UserModel.objects.only(
            "id",
            "name",
            "email",
            "is_active",
            "is_blocked",
            "is_verified",
            "date_joined",
        ).order_by("-date_joined")

        # Conditional orders count (PERFORMANCE)
        if include_orders:
            queryset = queryset.annotate(
                orders_count=Count("orders", distinct=True)
            )

        # Search
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search)
            )

        if status_filter == "active":
            queryset = queryset.filter(is_active=True, is_blocked=False)
        elif status_filter == "inactive":
            queryset = queryset.filter(is_active=False)
        elif status_filter == "blocked":
            queryset = queryset.filter(is_blocked=True)

        # Pagination
        paginator = AdminUserPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = AdminUserSerializer(page, many=True)

        return paginator.get_paginated_response({
            "stats": get_user_stats(),
            "results": serializer.data
        })
