from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "isAdmin": user.is_staff,
            "joinDate": user.date_joined, 
        },status=status.HTTP_200_OK)
