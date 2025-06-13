import logging

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.serializers import ChangePasswordSerializer, UserSerializer

logger = logging.getLogger(__name__)


@extend_schema(tags=["Profile"])
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Endpoint for retrieve and update users.

    - GET /profile/: Retrieve the authenticated user's profile.
    - PUT/PATCH /profile/: Update the authenticated user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Get the object to be updated.

        Returns:
            User: The authenticated user.
        """
        return self.request.user


@extend_schema(tags=["Profile"])
class ChangePasswordView(generics.UpdateAPIView):
    """
    Endpoint for change password.

    - PUT/PATCH /change-password/: Change the password of the authenticated user.
    """

    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Get the object to be updated.

        Returns:
            User: The authenticated user.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Update the password for the authenticated user.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: {"detail": "Password updated successfully"}.
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.warning(
                f"Error while changing password for user {user.email}: {str(e)}"
            )

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old_password": "Wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        logger.info(f"Password updated successfully for user {user.email}")

        return Response(
            {"detail": "Password updated successfully"}, status=status.HTTP_200_OK
        )
