from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.reviews.models.review_model import Review
from apps.reviews.serializers.review_create_serializer import ReviewCreateSerializer
from apps.reviews.serializers.review_list_serializer import ReviewListSerializer
from apps.reviews.utils.is_verified_purchase import is_verified_purchase
from apps.products.models.product_model import Product
from apps.reviews.pagination import ReviewPagination


class ProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


    def get(self, request, product_id):
        get_object_or_404(Product, id=product_id)

        queryset = (Review.objects.filter(product_id=product_id).select_related("user"))
        paginator = ReviewPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = ReviewListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, product_id):

        product = get_object_or_404(Product, id=product_id)
        user = request.user
        if Review.objects.filter(product=product, user=user).exists():
            return Response(
                {"detail": "You have already reviewed this product"},
                status=status.HTTP_400_BAD_REQUEST
            )


        verified = is_verified_purchase(user, product)

        serializer = ReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review = serializer.save(
            product=product,
            user=user,
            verified=is_verified_purchase(user, product)
        )
        full_serializer = ReviewListSerializer(review)

        return Response(full_serializer.data, status=status.HTTP_201_CREATED)
