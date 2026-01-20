from rest_framework import serializers
from apps.accounts.models.user_model import UserModel


class AdminUserSerializer(serializers.ModelSerializer):
    orders_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = UserModel
        fields = [
            "id",
            "name",
            "email",
            "is_active",
            "is_verified",
            "is_blocked",
            "is_staff",
            "auth_provider",
            "date_joined",
            "last_login",
            "orders_count",
        ]
        read_only_fields = fields
