from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from apps.accounts.serializers.signup_serializer import SignupSerializer
from apps.accounts.services.otp_service import OTPService
from apps.accounts.tasks import send_otp_email_task

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        try:
            otp = OTPService.create_otp(
                user=user,
                purpose="signup"
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        send_otp_email_task.delay(user.email, otp)

        return Response(
            {
                "detail": "Account created. Verify OTP to activate.",
                "next": "otp"
            },
            status=status.HTTP_201_CREATED
        )
