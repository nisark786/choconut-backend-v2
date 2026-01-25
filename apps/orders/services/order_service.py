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

        # Lock cart
        cart = Cart.objects.select_for_update().filter(user=user).first()
        if not cart or not cart.items.exists():
            raise ValueError("Cart is empty or not found")

        cart_items = cart.items.select_related("product")

        # STEP 1: Validate stock
        for item in cart_items:
            if item.product.stock < item.quantity:
                raise ValueError(
                    f"{item.product.name} is out of stock"
                )

        # STEP 2: Calculate total
        total_amount = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        # STEP 3: Create order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_status="PENDING"
        )

        # STEP 4: Create order items
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

        # STEP 5: Deduct stock (DB-safe)
        for item in cart_items:
            Product.objects.filter(id=item.product.id).update(
                stock=F("stock") - item.quantity
            )

        # STEP 6: Clear cart
        cart.items.all().delete()

        return order
