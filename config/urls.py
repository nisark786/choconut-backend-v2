
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path, include
from django.contrib import admin
from apps.accounts.views.health_check_view import health_check

schema_view = get_schema_view(
    openapi.Info(
        title="Choconut API",
        default_version='v1',
        description="API documentation for Choconut backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.products.urls')),
    path("api/cart/", include("apps.cart.urls")),
    path("api/orders/", include("apps.orders.urls")),
    path("api/payments/", include("apps.payments.urls")),
    path("api/wishlist/", include("apps.wishlist.urls")),
    path("api/", include("apps.reviews.urls")),
    path("api/admin/", include("apps.admin_panel.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/", include("apps.chatboat.urls")),

    path("health/", health_check),

    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
