from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from apps.accounts.serializers.login_serializer import LoginSerializer 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
class LoginView(APIView):
    permission_classes = [AllowAny]  

    @swagger_auto_schema(
            request_body=LoginSerializer,
            responses={ 200: "success" },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

       
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({
            "access": str(access),
            "user": {
                "userId": user.id,
                "name": user.name,
                "email": user.email,
                "isAdmin": user.is_staff,
            }
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,  
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response
