from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.serializers.google_serializer import GoogleAuthSerializer


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.context["user"]

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response(
            {
                "access": str(access),
                "user": {
                    "userId": user.id,
                    "name": user.name,
                    "email": user.email,
                    "isAdmin": user.is_staff,
                }
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response
