from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False)

    def validate(self, attrs):
        request = self.context["request"]

        refresh = request.COOKIES.get("refresh_token")

        if not refresh:
            raise serializers.ValidationError(
                "Refresh token not found."
            )

        self.token = RefreshToken(refresh)
        return attrs

    def save(self, **kwargs):
        self.token.blacklist()
