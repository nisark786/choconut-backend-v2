from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.accounts.models.user_model import UserModel


class TestStartOTPAPI(APITestCase):

    def test_start_otp_success(self):
        user = UserModel.objects.create_user(
            email="start@test.com",
            password="Test12345",
            name="Start"
        )

        response = self.client.post(
            reverse("otp-start"),
            {"email": user.email, "purpose": "signup"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_start_otp_user_not_found(self):
        response = self.client.post(
            reverse("otp-start"),
            {"email": "missing@test.com", "purpose": "signup"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_otp_already_verified(self):
        user = UserModel.objects.create_user(
            email="verified@test.com",
            password="Test12345",
            name="Verified",
            is_verified=True
        )

        response = self.client.post(
            reverse("otp-start"),
            {"email": user.email, "purpose": "signup"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
