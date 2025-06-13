import logging

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.serializers import RegisterSerializer

logger = logging.getLogger(__name__)


@extend_schema(tags=["Auth"])
class RegisterView(APIView):
    """
    Endpoint for registering a new user.

    - POST /register/: Create a new user.
    """

    permission_classes = [AllowAny]

    @extend_schema(auth=[])
    def post(self, request):
        """
        Handle user registration.

        Creates a new user and returns an access token.
        Also sets a refresh token as an HTTP-only cookie.

        Returns:
            Response: { "access": <access_token> }
        """
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

            logger.info(f"User {user.email} registered successfully")
            return response

        logger.warning(f"Login failed for email: {request.data.email}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Auth"])
class LoginView(TokenObtainPairView):
    """
    Endpoint for logging in a user.

    - POST /login/: Login a user.
    """

    permission_classes = [AllowAny]

    @extend_schema(auth=[])
    def post(self, request, *args, **kwargs):
        """
        Authenticate user and return access token.

        Sets a refresh token as an HTTP-only cookie.

        Returns:
            Response: { "access": <access_token> }
        """

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
        logger.info(f"User {request.data.email} logged in successfully")
        return response


@extend_schema(tags=["Auth"])
class LogoutView(APIView):
    """
    Endpoint for logout a user.

    - POST /logout/: Logout a user.
    """

    permission_classes = [AllowAny]

    @extend_schema(auth=[])
    def post(self, request):
        """
        Logout user and remove refresh token from cookie.

        Returns:
            Response: { "message": "Logged out successfully" }
        """
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

        logger.info(f"User {request.user.email} logged out successfully")

        return response


@extend_schema(tags=["Auth"])
class CookieTokenRefreshView(TokenRefreshView):
    """
    Endpoint for refreshing tokens using refresh token from cookies.

    - POST /token/refresh/: Refresh access token using refresh token.
    """

    permission_classes = [AllowAny]

    @extend_schema(auth=[])
    def post(self, request, *args, **kwargs):
        """
        Refresh a access and refresh token using refresh token.

        Automatically refresh refresh token to the response HTTP-only cookie.

        Returns:
            Response: { "access": <access_token> }
        """
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
            logger.warning(f"Error while refreshing tokens: {str(e)}")

            return Response(
                {
                    "detail": f"Error while refreshing tokens to user {request.user.email}: {str(e)}"
                },
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

        logger.info(f"User {request.user.email} refreshed tokens successfully")

        return response
