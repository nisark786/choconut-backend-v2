from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.models.user_model import UserModel
from apps.accounts.services.otp_service import OTPService
from apps.accounts.serializers.otp_serializer import OTPStartSerializer
from apps.accounts.serializers.otp_serializer import OTPVerifySerializer
from apps.accounts.utils.email import send_otp_email
from rest_framework_simplejwt.tokens import RefreshToken


class StartOTPView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = OTPStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        purpose = serializer.validated_data["purpose"]

        if "@" not in email:
            return Response(
                {"detail": "Only email OTP is supported"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if purpose == "signup":
            user = UserModel.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"detail": "Signup required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user.is_verified:
                return Response(
                    {"detail": "User already verified"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:  
            user = UserModel.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"detail": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        try:
            otp = OTPService.create_otp(user=user, purpose=purpose)
            send_otp_email(user.email, otp)
            return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class VerifyOTPView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        purpose = serializer.validated_data["purpose"]

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        valid, message = OTPService.verify_otp(
            user=user,
            otp=otp,
            purpose=purpose,
        )

        if not valid:
            return Response(
                {
                    "success": False,
                    "message": message
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        if purpose == "signup":
            user.is_verified = True
            user.is_active = True
            user.save(update_fields=["is_verified", "is_active"])

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        response =  Response({
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
                secure=True,
                samesite="None",
                max_age=7 * 24 * 60 * 60,
            )

        return response




class ResendOTPView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = OTPStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        purpose = serializer.validated_data["purpose"]

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        otp = OTPService.create_otp(
            user=user,
            purpose=purpose,
        )

        send_otp_email(user.email, otp)

        return Response(
            {"detail": "OTP resent successfully"},
            status=status.HTTP_200_OK
        )
