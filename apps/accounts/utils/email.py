from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(email, otp):
    send_mail(
        subject="Your verification code",
        message=f"Your OTP is {otp}. It expires in 5 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
