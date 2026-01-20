import razorpay
from django.conf import settings


class RazorpayService:

    @staticmethod
    def get_client():
        return razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    @staticmethod
    def create_order(amount, receipt):
        client = RazorpayService.get_client()
        return client.order.create({
            "amount": int(amount * 100),  # convert to paise
            "currency": "INR",
            "receipt": receipt,
            "payment_capture": 1
        })

    @staticmethod
    def verify_signature(data):
        client = RazorpayService.get_client()
        client.utility.verify_payment_signature(data)
