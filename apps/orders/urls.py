from django.urls import path
from .views.checkout_view import CheckoutView
from .views.order_address_view import OrderAddressView
from .views.order_detail_view import OrderDetailView
from .views.order_list_view import OrderListView
from .views.order_cancel_view import CancelOrderView

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("<int:order_id>/address/", OrderAddressView.as_view()),
    path("address/", OrderAddressView.as_view()),
    path("<int:order_id>/", OrderDetailView.as_view()),
    path("<int:order_id>/cancel/", CancelOrderView.as_view()),

]
