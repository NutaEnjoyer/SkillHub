from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from drf_spectacular.utils import extend_schema

import logging


logger = logging.getLogger(__name__)


@extend_schema(tags=["Profile"])
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
