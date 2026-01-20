from django.urls import path
from apps.admin_panel.views.user_list_view import AdminUserListView
from apps.admin_panel.views.user_action_view import AdminUserActionView
from apps.admin_panel.views.user_details_view import AdminUserDetailView
from apps.admin_panel.views.product_detail_view import AdminProductDetailView
from apps.admin_panel.views.product_list_create_view import AdminProductListCreateView
from apps.admin_panel.views.order_view import AdminOrderDetailView,AdminOrderListView
from apps.admin_panel.views.dashboard_view import AdminDashboardOverviewView


urlpatterns = [
    path("dashboard/", AdminDashboardOverviewView.as_view()),
    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("users/<int:id>/action/", AdminUserActionView.as_view(), name="admin-actions"),
    path("users/<int:id>/", AdminUserDetailView.as_view(),name="admin-users-details"),
    path("products/", AdminProductListCreateView.as_view(), name="admin-products"),
    path("products/<int:product_id>/", AdminProductDetailView.as_view(), name="admin-product-detail"),
    path("orders/", AdminOrderListView.as_view(), name="admin-order-list"),
    path("orders/<int:order_id>/", AdminOrderDetailView.as_view(), name="admin-order-detail"),
]
