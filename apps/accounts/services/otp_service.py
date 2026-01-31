import random
import hashlib
from django.db import transaction
from apps.accounts.models.otp_model import VerificationOTP
from django.core.cache import cache


OTP_EXPIRY_MINUTES = 5
MAX_ATTEMPTS = 5
OTP_COOLDOWN_SECONDS = 60


class OTPService:

    @staticmethod
    def _generate_otp() -> str:
        return f"{random.randint(100000, 999999)}"

    @staticmethod
    def _hash_otp(otp: str) -> str:
        return hashlib.sha256(otp.encode()).hexdigest()

    @staticmethod
    def _invalidate_old_otps(user, purpose):
        VerificationOTP.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False
        ).update(is_used=True)

    @classmethod
    @transaction.atomic
    def create_otp(cls, user, purpose) -> str:
        
        cls._check_cooldown(user, purpose)
        
        cls._invalidate_old_otps(user, purpose)

        otp = cls._generate_otp()
        otp_hash = cls._hash_otp(otp)

        VerificationOTP.objects.create(
            user=user,
            otp_hash=otp_hash,
            purpose=purpose
        )

        return otp  

    @classmethod
    def verify_otp(cls, user, otp, purpose):
        
        try:
            otp_obj = VerificationOTP.objects.filter(
                user=user,
                purpose=purpose,
                is_used=False
            ).latest("created_at")
        except VerificationOTP.DoesNotExist:
            return False, "OTP not found"

        if otp_obj.is_expired():
            otp_obj.is_used = True
            otp_obj.save(update_fields=["is_used"])
            return False, "OTP expired"

        if otp_obj.attempts >= MAX_ATTEMPTS:
            otp_obj.is_used = True
            otp_obj.save(update_fields=["is_used"])
            return False, "Too many attempts"

        if cls._hash_otp(otp) != otp_obj.otp_hash:
            otp_obj.attempts += 1
            otp_obj.save(update_fields=["attempts"])
            return False, "Invalid OTP"

        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used"])

        return True, "OTP verified"


    @staticmethod
    def _check_cooldown(user, purpose):
        cache_key = f"otp_cooldown_{user.id}_{purpose}"
        
        if cache.get(cache_key):
            raise ValueError("Please wait 60 seconds")
            

        cache.set(cache_key, "true", timeout=60)