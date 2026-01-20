from django.urls import path
from apps.wishlist.views.wishlist_view import WishlistView
from apps.wishlist.views.toggle_wishlist_view import ToggleWishlistView

urlpatterns = [
    path("", WishlistView.as_view()),
    path("toggle/", ToggleWishlistView.as_view()),
]
