from django.test import TestCase
from apps.accounts.services.otp_service import OTPService
from apps.accounts.models.user_model import UserModel


class TestOTPService(TestCase):

    def test_verify_otp_success(self):
        user = UserModel.objects.create_user(
            email="test@example.com",
            password="Test12345",
            name="Test"
            )
        
        otp = OTPService.create_otp(user, "signup")

        valid, message = OTPService.verify_otp(
            user=user,
            otp=otp,
            purpose="signup"
            )
        
        self.assertTrue(valid)
        self.assertEqual(message, "OTP verified")

    def test_verify_wrong_otp(self):
        user = UserModel.objects.create_user(
            email="wrong@example.com",
            password="Test12345",
            name="Wrong"
        )

        OTPService.create_otp(user, "signup")

        valid, message = OTPService.verify_otp(
            user=user,
            otp="000000",
            purpose="signup"
        )

        self.assertFalse(valid)
        self.assertEqual(message, "Invalid OTP")




