from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.wishlist.models.wishlist_model import Wishlist
from apps.wishlist.serializers.wishlist_serializer import WishlistSerializer
from apps.wishlist.services.wishlist_service import WishlistService


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user).prefetch_related(
            'items__product'
        ).first()
        if not wishlist:
            wishlist = WishlistService.get_or_create_wishlist(request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data,status=status.HTTP_200_OK)


