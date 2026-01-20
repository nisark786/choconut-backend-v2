from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.accounts.models.user_model import UserModel


class TestSignupEdgeCases(APITestCase):

    def test_signup_existing_active_user(self):
        UserModel.objects.create_user(
            email="active@test.com",
            password="Test12345",
            name="Active",
            is_active=True,
            is_verified=True
        )

        response = self.client.post(
            reverse("signup"),
            {
                "name": "Active",
                "email": "active@test.com",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_existing_inactive_user(self):
        UserModel.objects.create_user(
            email="inactive@test.com",
            password="Test12345",
            name="Inactive",
            is_active=False,
            is_verified=False
        )

        response = self.client.post(
            reverse("signup"),
            {
                "name": "Inactive Updated",
                "email": "inactive@test.com",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_invalid_payload(self):
        response = self.client.post(
            reverse("signup"),
            {"email": "bad@test.com"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
