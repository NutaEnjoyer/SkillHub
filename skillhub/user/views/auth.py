from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
import logging


logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("RegisterView: POST request received")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response(
                {"access": access_token},
                status=status.HTTP_201_CREATED,
            )

            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                max_age=int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
                samesite="Lax",
            )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.pop("refresh")

        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                max_age=int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
                samesite="Lax",
            )

        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError as e:
                logger.warning(f"Logout failed to blacklist token: {str(e)}")

        response = Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
        response.delete_cookie("refresh_token")
        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token not provided in cookies"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response(
                {"detail": f"Error while refreshing tokens: {str(e)}"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = serializer.validated_data.get("access")
        new_refresh_token = serializer.validated_data.get("refresh")

        response = Response({"access": access_token}, status=status.HTTP_200_OK)

        if new_refresh_token:
            response.set_cookie(
                "refresh_token",
                new_refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
                path="/",
            )

        return response


