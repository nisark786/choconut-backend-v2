from django.db import transaction
from decimal import Decimal
from apps.orders.models.order_item_model import OrderItem
from apps.orders.models.order_model import Order
from apps.cart.models.cart_item_model import CartItem
from apps.cart.models.cart_model import Cart


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user):
        
        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            raise ValueError("Cart is empty or not found")

        total_amount = sum(item.product.price * item.quantity for item in cart.items.all())

        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_status="PENDING"
        )

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            ) for item in cart.items.all()
        ]
        OrderItem.objects.bulk_create(order_items) 

        return order
