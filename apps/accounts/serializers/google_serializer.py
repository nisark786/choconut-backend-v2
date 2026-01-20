from rest_framework import serializers
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from apps.accounts.models.user_model import UserModel


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate_token(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
        except ValueError:
            raise serializers.ValidationError("Invalid Google token")

        email = idinfo.get("email")
        name = idinfo.get("name", "")

        if not email:
            raise serializers.ValidationError("Email not provided by Google")

        user, created = UserModel.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "auth_provider": "google",
                "is_active": True,
                "is_verified": True,
            }
        )

  
        if not created and user.auth_provider != "google":
            raise serializers.ValidationError(
                "Account exists with email/password login"
            )

        self.context["user"] = user
        return token
