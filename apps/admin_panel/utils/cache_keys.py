ADMIN_USER_STATS_CACHE_KEY = "admin_user_stats"
ADMIN_ORDER_STATS_CACHE_KEY = "admin_order_stats"

def clear_admin_user_stats_cache():
    from django.core.cache import cache
    cache.delete(ADMIN_USER_STATS_CACHE_KEY)


def clear_admin_order_stats_cache():
    from django.core.cache import cache
    cache.delete(ADMIN_ORDER_STATS_CACHE_KEY)
