
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from  rest_framework import status 

class CookieTokenRefreshView(TokenRefreshView):

    permission_classes = []
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")
        if not refresh:
            return Response({"detail": "Refresh token missing"}, status=status.HTTP_401_UNAUTHORIZED)

        request.data["refresh"] = refresh
        response = super().post(request, *args, **kwargs)

        # Update refresh cookie
        if "refresh" in response.data:
            response.set_cookie(
                key="refresh_token",
                value=response.data["refresh"],
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=7*24*60*60,
            )
        return response
