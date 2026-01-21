from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.orders.models.order_model import Order
from apps.orders.models.order_item_model import OrderItem
from apps.products.models.product_model import Product
from apps.accounts.models.user_model import UserModel
from apps.admin_panel.permissions.admin_permissions import IsAdminUser


class AdminDashboardOverviewView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # === BASIC STATS ===
        total_revenue = Order.objects.filter(
            payment_status="PAID"
        ).aggregate(total=Sum("total_amount"))["total"] or 0

        stats = {
            "total_revenue": total_revenue,
            "total_orders": Order.objects.count(),
            "total_products": Product.objects.count(),
            "total_users": UserModel.objects.count(),
        }

        # === MONTHLY REVENUE ===
        monthly_qs = (
            Order.objects
            .filter(payment_status="PAID")
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(revenue=Sum("total_amount"))
            .order_by("month")
        )

        monthly_revenue = [
            {
                "month": m["month"].strftime("%b"),
                "revenue": m["revenue"]
            }
            for m in monthly_qs
        ]

        # === ORDER STATUS ===
        order_status = (
            Order.objects
            .values("order_status")
            .annotate(count=Count("id"))
        )

        # === TOP PRODUCTS ===
        top_products = (
            OrderItem.objects
            .values("product__name")
            .annotate(sales=Sum("quantity"))
            .order_by("-sales")[:5]
        )

        return Response({
            "stats": stats,
            "monthly_revenue": monthly_revenue,
            "order_status": order_status,
            "top_products": [
                {
                    "name": p["product__name"],
                    "sales": p["sales"]
                }
                for p in top_products
            ]
        })
