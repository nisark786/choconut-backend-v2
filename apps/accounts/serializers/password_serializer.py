from rest_framework import serializers

class SetPasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
