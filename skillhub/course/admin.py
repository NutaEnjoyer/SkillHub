from course.models import Category, Course, Lesson, Module
from django.contrib import admin
from django.db.models import Avg
from review.models import Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Custom admin class for managing categories.

    Display the category's name and description.
    Search by name and description.
    """

    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Custom admin class for managing courses.

    Display the course's title, author, average rating, category, level,
    created_at, and updated_at.
    Filter by category, level, created_at, and updated_at.
    Search by title, description, and author's username.
    Order by created_at in descending order.
    Exclude the author field from the form.
    """

    list_display = (
        "title",
        "author",
        "avg_rate",
        "category",
        "level",
        "created_at",
        "updated_at",
    )
    list_filter = ("category", "level", "created_at", "updated_at")
    search_fields = ("title", "description", "author__username")
    ordering = ("-created_at",)
    exclude = ("author",)

    def avg_rate(self, obj):
        """
        Aggregate the average rating for the course.
        """

        avg = Review.objects.filter(course=obj).aggregate(avg_rating=Avg("rating"))[
            "avg_rating"
        ]
        return round(avg, 1) if avg else 0

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to set the author field.
        """

        if not obj.pk or not obj.author_id:  # Если объект новый или автор не установлен
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """
    Custom admin class for managing modules.

    Display the module's title, course, and order.
    Filter by course and order.
    Search by title and course's title.
    """

    list_display = ("title", "course", "order")
    list_filter = ("course", "order")
    search_fields = ("title", "course__title")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Custom admin class for managing lessons.

    Display the lesson's title, module, and order.
    Filter by module and order.
    Search by title and module's title.
    """

    list_display = ("title", "module", "order")
    list_filter = ("module", "order")
    search_fields = ("title", "module__title")
