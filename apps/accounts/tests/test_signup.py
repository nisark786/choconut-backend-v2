from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.accounts.models.user_model import UserModel
from unittest.mock import patch

class TestSignupFlow(APITestCase):

    @patch("apps.accounts.services.otp_service.OTPService._generate_otp")
    def test_signup_and_verify_otp(self, mock_generate_otp):
        mock_generate_otp.return_value = "123456"  

        signup_url = reverse("signup")
        user_data = {
            "name": "EndToEnd Test",
            "email": "e2e@test.com",
            "password": "Test12345"
        }
        response = self.client.post(signup_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["next"], "otp")

        # Step 2: Fetch user from DB
        user = UserModel.objects.get(email="e2e@test.com")

        # Step 3: Verify OTP
        verify_url = reverse("otp-verify")
        otp_data = {
            "email": user.email,
            "otp": "123456",  # our mocked OTP
            "purpose": "signup"
        }
        response = self.client.post(verify_url, otp_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "OTP verified successfully")

        # Step 4: Check user status
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_verified)

        # Step 5: JWT tokens exist
        self.assertIn("access", response.data)
