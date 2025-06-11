from django.contrib import admin
from review.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'user', 'rating', 'title', 'content')
    list_filter = ('course', 'user', 'rating')
    search_fields = ('course__title', 'user__email', 'title')
    ordering = ('-created_at',)
