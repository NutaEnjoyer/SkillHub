from django.contrib import admin
from course.models import Category, Course, Module, Lesson
from review.models import Review
from django.db.models import Avg


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'avg_rate', 'category', 'level', 'created_at', 'updated_at')
    list_filter = ('category', 'level', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-created_at', )
    exclude = ('author',) 

    def avg_rate(self, obj):
        avg = Review.objects.filter(course=obj).aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 1) if avg else 0

    def save_model(self, request, obj, form, change):
        if not obj.pk or not obj.author_id:  # Если объект новый или автор не установлен
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course', 'order')
    search_fields = ('title', 'course__title')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    list_filter = ('module', 'order')
    search_fields = ('title', 'module__title')
