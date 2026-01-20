from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.wishlist.services.wishlist_service import WishlistService


class ToggleWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"detail": "Product ID required"}, status=400)

        is_added = WishlistService.toggle_product(request.user, product_id)
        
        status_msg = "added to" if is_added else "removed from"
        return Response({
            "is_added": is_added,
            "message": f"Product {status_msg} wishlist"
        }, status=status.HTTP_200_OK)