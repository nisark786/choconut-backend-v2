from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.accounts.models.user_model import UserModel

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", "").lower().strip()
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        user = UserModel.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        if getattr(user, "is_blocked", False):
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active or not getattr(user, "is_verified", False):
            raise serializers.ValidationError("Invalid email or password")
    
        attrs["user"] = user
        return attrs
