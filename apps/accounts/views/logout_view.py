from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.serializers.logout_serializer import LogoutSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(
            data={},
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_200_OK
        )
        
        response.delete_cookie("refresh_token")

        return response
