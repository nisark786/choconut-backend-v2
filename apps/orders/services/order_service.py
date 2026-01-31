from django.db import transaction
from django.db.models import F
from apps.orders.models.order_item_model import OrderItem
from apps.orders.models.order_model import Order
from apps.cart.models.cart_model import Cart
from apps.products.models.product_model import Product


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user):

        cart = Cart.objects.select_for_update().filter(user=user).first()
        if not cart or not cart.items.exists():
            raise ValueError("Cart is empty or not found")

        cart_items = cart.items.select_related("product")

        
        for item in cart_items:
            if item.product.stock < item.quantity:
                raise ValueError(
                    f"{item.product.name} is out of stock"
                )

        
        total_amount = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_status="PENDING"
        )

 
        order_items = []
        for item in cart_items:
            order_items.append(
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            )

        OrderItem.objects.bulk_create(order_items)

        
        for item in cart_items:
            Product.objects.filter(id=item.product.id).update(
                stock=F("stock") - item.quantity
            )

      
        cart.items.all().delete()

        return order
