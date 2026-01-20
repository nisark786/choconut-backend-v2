from apps.orders.models.order_model import Order


def is_verified_purchase(user, product):
    return Order.objects.filter(
        user=user,
        order_status="DELIVERED",
        items__product=product
    ).exists()
