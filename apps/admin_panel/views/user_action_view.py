from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.admin_panel.utils.cache_keys import clear_admin_user_stats_cache
from django.db import transaction
from apps.accounts.models.user_model import UserModel
from apps.admin_panel.permissions.admin_permissions import IsAdminUser
from apps.admin_panel.serializers.user_action_serializer import AdminUserActionSerializer


class AdminUserActionView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            user = UserModel.objects.only(
                "id", "is_blocked", "is_staff"
            ).get(id=id)
        except UserModel.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AdminUserActionSerializer(
            data=request.data,
            context={
                "request": request,
                "target_user": user,
            },
        )
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data["action"]

        if action == "block":
            user.is_blocked = True
        elif action == "unblock":
            user.is_blocked = False
        elif action == "make_admin":
            user.is_staff = True
        elif action == "remove_admin":
            user.is_staff = False

        user.save(update_fields=["is_blocked", "is_staff"])

        transaction.on_commit(clear_admin_user_stats_cache)

        return Response(
            {
                "id": user.id,
                "action": action,
                "message": "Action applied successfully",
            },
            status=status.HTTP_200_OK,
        )
