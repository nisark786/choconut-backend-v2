from django.db.models import Sum, Count
from apps.orders.models.order_model import Order
from apps.products.models.product_model import Product
from rest_framework.views import APIView
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from apps.accounts.models.user_model import UserModel
from rest_framework.response import Response

class AdminDashboardOverviewView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_revenue = Order.objects.filter(
            payment_status="PAID"
        ).aggregate(total=Sum("total"))["total"] or 0

        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        total_users = UserModel.objects.count()

        return Response({
            "stats": {
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "total_products": total_products,
                "total_users": total_users
            }
        })
