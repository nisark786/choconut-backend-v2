from django.db import transaction
from apps.cart.models.cart_model import Cart
from apps.cart.models.cart_item_model import CartItem
from apps.products.models.product_model import Product
from django.db.models import F


class CartService:

    @staticmethod
    def get_or_create_cart(user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    @transaction.atomic
    def add_product(user, product_id, quantity=1):
        cart = CartService.get_or_create_cart(user)
        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": quantity,
                "price_at_added": product.price,
            }
        )

        if not created:
            item.quantity = F("quantity") + quantity
            item.save(update_fields=["quantity"])
            item.refresh_from_db()

        return cart

    @staticmethod
    def remove_product(user, product_id):
        cart = CartService.get_or_create_cart(user)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    @staticmethod
    def update_quantity(user, product_id, quantity):
        cart = CartService.get_or_create_cart(user)
        item = CartItem.objects.get(cart=cart, product_id=product_id)

        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

    @staticmethod
    def clear_cart(user):
        cart = CartService.get_or_create_cart(user)
        cart.items.all().delete()
