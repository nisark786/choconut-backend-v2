from django.urls import path
from apps.reviews.views.product_review_view import ProductReviewView

urlpatterns = [
    path(
        "products/<int:product_id>/reviews/",
        ProductReviewView.as_view(),
        name="product-review"
    ),
]

