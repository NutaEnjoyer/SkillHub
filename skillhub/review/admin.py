from django.contrib import admin
from review.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Review model.

    Display the review's ID, course, user, rating, title, and content.
    Filter by course, user, and rating.
    Search by course title, user email, review title
    Ordering by the creation date.
    """

    list_display = ("id", "course", "user", "rating", "title", "content")
    list_filter = ("course", "user", "rating")
    search_fields = ("course__title", "user__email", "title")
    ordering = ("-created_at",)
