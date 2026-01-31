from rest_framework import serializers
from apps.accounts.models.user_model import UserModel


class AdminUserActionSerializer(serializers.Serializer):
    ACTION_CHOICES = (
        ("block", "Block user"),
        ("unblock", "Unblock user"),
        ("make_admin", "Promote to admin"),
        ("remove_admin", "Remove admin role"),
    )

    action = serializers.ChoiceField(choices=ACTION_CHOICES)

    def validate(self, attrs):
        request = self.context["request"]
        target_user: UserModel = self.context["target_user"]


        if target_user.id == request.user.id:
            raise serializers.ValidationError(
                "You cannot perform this action on yourself"
            )

        action = attrs["action"]

        if action == "block" and target_user.is_blocked:
            raise serializers.ValidationError("User is already blocked")

        if action == "unblock" and not target_user.is_blocked:
            raise serializers.ValidationError("User is not blocked")

        if action == "make_admin" and target_user.is_staff:
            raise serializers.ValidationError("User is already an admin")

        if action == "remove_admin":
            if not UserModel.objects.filter(is_staff=True).exclude(id=target_user.id).exists():
                raise serializers.ValidationError(
                    "You cannot remove the last admin user"
                )


        return attrs
