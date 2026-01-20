from django.urls import path
from .views.create_payment_view import CreatePaymentView
from .views.verify_payment_view import VerifyPaymentView

urlpatterns = [
    path("create/", CreatePaymentView.as_view()),
    path("verify/", VerifyPaymentView.as_view()),
]
