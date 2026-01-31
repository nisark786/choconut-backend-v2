from apps.wishlist.models.wishlist_model import Wishlist
from apps.wishlist.models.wishlist_item_model import WishlistItem
from apps.products.models.product_model import Product


class WishlistService:

    @staticmethod
    def get_or_create_wishlist(user):
        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        return wishlist

    @staticmethod
    def add_product(user, product_id):
        wishlist = WishlistService.get_or_create_wishlist(user)

        WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product_id=product_id
        )

        return wishlist

    @staticmethod
    def remove_product(user, product_id):
        wishlist = WishlistService.get_or_create_wishlist(user)
        WishlistItem.objects.filter(
            wishlist=wishlist,
            product_id=product_id
        ).delete()

    @staticmethod
    def toggle_product(user, product_id):
        wishlist = WishlistService.get_or_create_wishlist(user)
        item_queryset = WishlistItem.objects.filter(wishlist=wishlist, product_id=product_id)
        
        if item_queryset.exists():
            item_queryset.delete()
            return False 
        else:
            WishlistItem.objects.create(wishlist=wishlist, product_id=product_id)
            return True 
