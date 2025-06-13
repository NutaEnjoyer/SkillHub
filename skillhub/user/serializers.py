from course.serializers import CourseSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register serializer for user registration.

    - `email`: The email address of the user.
    - `full_name`: The full name of the user.
    - `password`: The password of the user.
    - `role`: The role of the user (e.g., "STUDENT", "INSTRUCTOR", "ADMIN").
    """

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("email", "full_name", "password", "role")

    def create(self, validated_data):
        """
        Create a new user with the provided data.

        Args:
            validated_data (dict): The validated data for user creation.

        Returns:
            User: The created user.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for get user details.

    - `id`: The ID of the user.
    - `email`: The email address of the user.
    - `full_name`: The full name of the user.
    - `role`: The role of the user (e.g., "STUDENT", "INSTRUCTOR", "ADMIN").
    - `enrolled_courses`: The courses enrolled by the user.
    """

    enrolled_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "role", "enrolled_courses")


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the password.

    - `old_password`: The old password of the user.
    - `new_password`: The new password of the user.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
