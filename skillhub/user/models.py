from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom manager for the User model with custom methods for creating users and superusers.

    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password of the user. Defaults to None.
            **extra_fields: Additional fields to be set on the user.

        Raises:
            ValueError: If the email field is not set.

        Returns:
            User: The created user.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.

        Sets:
            - is_staff: True
            - is_superuser: True
            - role: ADMIN

        Args:
            email (str): The email address of the superuser.
            password (str, optional): The password of the superuser. Defaults to None.
            **extra_fields: Additional fields to be set on the superuser.

        Returns:
            User: The created superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model representing a user.

    - `email`: The email address of the user.
    - `full_name`: The full name of the user.
    - `role`: The role of the user (e.g., admin, instructor, student).
    - `is_active`: Indicates whether the user is active or not.
    - `is_staff`: Indicates whether the user has staff privileges.

    Authentication:
        - `email`: The email address is used as unique identifier for authentication.

    Roles:
        - `ADMIN`: Admin role. Full access to the system
        - `INSTRUCTOR`: Instructor role. Can create and manage courses.
        - `STUDENT`: Student role. Can enroll in courses and access course content.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        INSTRUCTOR = "instructor", "Instructor"
        STUDENT = "student", "Student"

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "role"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"User <{self.email}> ({self.get_role_display()})"
