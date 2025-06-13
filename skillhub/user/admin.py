from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the User model.

    Displays the user's email, full name, role, and a list of enrolled courses.
    Allows searching by email and full name, and filtering by role.
    """

    list_display = ("email", "full_name", "role", "enrolled_courses_list")
    search_fields = ("email", "full_name")
    list_filter = ("role",)

    def enrolled_courses_list(self, obj):
        return ", ".join([course.title for course in obj.enrolled_courses.all()])

    enrolled_courses_list.short_description = "Enrolled Courses"
