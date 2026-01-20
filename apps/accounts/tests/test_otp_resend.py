from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.accounts.models.user_model import UserModel


class TestResendOTPAPI(APITestCase):

    def test_resend_otp_success(self):
        user = UserModel.objects.create_user(
            email="resend@test.com",
            password="Test12345",
            name="Resend"
        )

        response = self.client.post(
            reverse("otp-resend"),
            {"email": user.email, "purpose": "signup"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resend_otp_user_not_found(self):
        response = self.client.post(
            reverse("otp-resend"),
            {"email": "missing@test.com", "purpose": "signup"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
