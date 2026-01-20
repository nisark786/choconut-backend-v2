from celery import shared_task
from datetime import timedelta
from django.utils import timezone



@shared_task(name="apps.accounts.tasks.send_otp_email_task")
def send_otp_email_task(email, otp):
    from apps.accounts.utils.email import send_otp_email
    send_otp_email(email, otp)


@shared_task
def cleanup_expired_otps():
    from apps.accounts.models.otp_model import VerificationOTP      
    cutoff = timezone.now() - timedelta(days=1)
    VerificationOTP.objects.filter(created_at__lt=cutoff).delete()