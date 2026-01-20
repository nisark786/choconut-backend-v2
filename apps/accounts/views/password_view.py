from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models.user_model import UserModel

class SetPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        user_id = request.data.get("user_id")
        password = request.data.get("password")

        if not user_id or not password:
            return Response(
                {"detail": "User ID and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_verified:
            return Response({"detail": "Please verify your phone/email first"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.is_active = True
        user.save(update_fields=["password","is_active"])

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "detail": "Password set successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                },
            },
            status=status.HTTP_200_OK
        )
