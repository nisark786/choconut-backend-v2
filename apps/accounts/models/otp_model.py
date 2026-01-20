from django.db import models
from django.utils import timezone
from .user_model import UserModel


class VerificationOTP(models.Model):

    PURPOSE_CHOICES = (
        ("signup", "Signup Verification"),
        ("login", "Login OTP"),
        ("reset", "Password Reset"),
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="email_otps"
    )

    otp_hash = models.CharField(max_length=128)

    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES
    )

    attempts = models.PositiveSmallIntegerField(default=0)

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "purpose", "created_at"]),
        ]

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"EmailOTP(user={self.user_id}, purpose={self.purpose})"
