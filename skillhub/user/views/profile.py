from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

import logging


logger = logging.getLogger(__name__)


@extend_schema(tags=["Profile"])
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Profile"])
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        ) 

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Password updated successfully"}, status=status.HTTP_200_OK
        )
