from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user

        if user.auth_provider != "email":
            raise serializers.ValidationError({
                "auth_provider": "Password change not allowed for Google accounts"
            })

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({
                "old_password": "Old password is incorrect"
            })

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })

        
        if user.check_password(attrs["new_password"]):
            raise serializers.ValidationError({
                "new_password": "New password cannot be same as old password"
            })

        return attrs

