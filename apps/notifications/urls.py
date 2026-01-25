from django.urls import path
from .views import (NotificationListView,
                    MarkNotificationReadView,
                    AddNotifyMeView,
                    RemoveNotifyMeView,
                    NotifyMeListView,
                    AdminNotificationListView,
                    AdminBroadcastView
                    )

urlpatterns = [
    path('admin/', AdminNotificationListView.as_view()),
    path('admin/broadcast/', AdminBroadcastView.as_view()),


    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='mark-read'),
    path('notify-me/', AddNotifyMeView.as_view(), name='add-notify'),
    path('notify-me/<int:product_id>/', RemoveNotifyMeView.as_view(), name='remove-notify'),
    path('notify-me/list/', NotifyMeListView.as_view(), name='notify-me-list'), 
]