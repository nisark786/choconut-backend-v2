from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.accounts.models.user_model import UserModel


class TestLoginAPI(APITestCase):

    def test_login_missing_email_or_password(self):
        response = self.client.post(
            reverse("login"),
            {"email": "test@test.com"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Email and password are required")


    def test_login_user_not_found(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "nouser@test.com",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "User not found")


    def test_login_blocked_user(self):
        UserModel.objects.create_user(
            email="blocked@test.com",
            password="Test12345",
            name="Blocked",
            is_active=True,
            is_verified=True,
            is_blocked=True
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "blocked@test.com",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "User blocked")


    def test_login_user_not_active_or_verified(self):
        UserModel.objects.create_user(
            email="inactive@test.com",
            password="Test12345",
            name="Inactive",
            is_active=False,
            is_verified=False
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "inactive@test.com",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "User not active or verified")



    def test_login_wrong_password(self):
        UserModel.objects.create_user(
            email="wrongpass@test.com",
            password="Correct123",
            name="Wrong Pass",
            is_active=True,
            is_verified=True
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "wrongpass@test.com",
                "password": "WrongPassword"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid password")



    def test_login_success(self):
        user = UserModel.objects.create_user(
            email="success@test.com",
            password="Test12345",
            name="Success",
            is_active=True,
            is_verified=True
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "success@test.com",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)



    def test_login_email_normalization(self):
        UserModel.objects.create_user(
            email="normalize@test.com",
            password="Test12345",
            name="Normalize",
            is_active=True,
            is_verified=True
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "  NORMALIZE@TEST.COM  ",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_login_without_is_blocked_field(self):
        user = UserModel.objects.create_user(
            email="safe@test.com",
            password="Test12345",
            name="Safe",
            is_active=True,
            is_verified=True
        )

        # Simulate missing attribute
        if hasattr(user, "is_blocked"):
            delattr(user, "is_blocked")

        response = self.client.post(
            reverse("login"),
            {
                "email": "safe@test.com",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_login_inactive_but_verified(self):
        UserModel.objects.create_user(
            email="half@test.com",
            password="Test12345",
            name="Half",
            is_active=False,
            is_verified=True
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "half@test.com",
                "password": "Test12345"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
