from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.accounts.models.user_model import UserModel
from apps.accounts.services.otp_service import OTPService


class TestVerifyOTPAPI(APITestCase):

    def test_verify_otp_success(self):
        user = UserModel.objects.create_user(
            email="api@test.com",
            password="Test12345",
            name="API Test"
        )

        otp = OTPService.create_otp(user, "signup")

        url = reverse("otp-verify")  # name in urls.py

        data = {
            "email": user.email,
            "otp": otp,
            "purpose": "signup"
        }

        response = self.client.post(url, data, format="json")


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "OTP verified successfully")


    def test_verify_otp_wrong_code(self):
        user = UserModel.objects.create_user(
            email="wrong@test.com",
            password="Test12345",
            name="Wrong OTP"
        )

        OTPService.create_otp(user, "signup")

        url = reverse("otp-verify")

        data = {
            "email": user.email,
            "otp": "000000",  
            "purpose": "signup"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Invalid OTP")




    def test_verify_otp_expired(self):
        user = UserModel.objects.create_user(
            email="expired@test.com",
            password="Test12345",
            name="Expired Test"
        )

        otp = OTPService.create_otp(user, "signup")

        otp_obj = user.email_otps.latest("created_at")
        otp_obj.created_at -= timedelta(minutes=6)  # OTP expired (older than 5 min)
        otp_obj.save()

        url = reverse("otp-verify")

        data = {
            "email": user.email,
            "otp": otp,
            "purpose": "signup"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "OTP expired")


    def test_verify_otp_reuse_blocked(self):
        user = UserModel.objects.create_user(
            email="reuse@test.com",
            password="Test12345",
            name="Reuse Test"
        )

        otp = OTPService.create_otp(user, "signup")

        url = reverse("otp-verify")
        data = {
            "email": user.email,
            "otp": otp,
            "purpose": "signup"
        }

        # First use (should succeed)
        response1 = self.client.post(url, data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertTrue(response1.data["success"])

        # Second use (should fail)
        response2 = self.client.post(url, data, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response2.data["success"])
        self.assertEqual(response2.data["message"], "OTP not found")



    def test_verify_otp_max_attempts(self):
        user = UserModel.objects.create_user(
            email="maxattempts@test.com",
            password="Test12345",
            name="Max Attempts Test"
        )

        OTPService.create_otp(user, "signup")
        url = reverse("otp-verify")

        # Try 5 wrong OTPs
        for i in range(5):
            response = self.client.post(url, {
                "email": user.email,
                "otp": "000000",
                "purpose": "signup"
            }, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Sixth attempt should indicate too many attempts
        response = self.client.post(url, {
            "email": user.email,
            "otp": "000000",
            "purpose": "signup"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Too many attempts")



    def test_otp_cannot_be_used_twice(self):
        # Step 1: Create inactive user
        user = UserModel.objects.create_user(
            email="reuse@test.com",
            password="Test12345",
            name="Reuse OTP"
        )
        # Step 2: Generate OTP
        otp = OTPService.create_otp(user, purpose="signup")
        url = reverse("otp-verify")
        payload = {
            "email": user.email,
            "otp": otp,
            "purpose": "signup"
        }
        # Step 3: First verification (should succeed)
        response1 = self.client.post(url, payload, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertTrue(response1.data["success"])
        # Step 4: Second verification using SAME OTP (must fail)
        response2 = self.client.post(url, payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        # IMPORTANT: do NOT assume message text exactly
        self.assertFalse(response2.data["success"])