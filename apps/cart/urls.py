from django.urls import path
from apps.cart.views.cart_view import CartView
from apps.cart.views.add_to_cart_view import AddToCartView
from apps.cart.views.update_cart_item_view import UpdateCartItemView
from apps.cart.views.remove_cart_item_view import RemoveCartItemView

urlpatterns = [
    path("", CartView.as_view()),
    path("add/", AddToCartView.as_view()),
    path("update/", UpdateCartItemView.as_view()),
    path("remove/", RemoveCartItemView.as_view()),
]
