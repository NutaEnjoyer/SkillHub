from rest_framework import viewsets, permissions
from course.models import Category, Course, Module, Lesson
from course.serializers import (
    CategorySerializer,
    CourseSerializer,
    ModuleSerializer,
    LessonSerializer,
)
from core.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=["Course"])
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=["Module"])
class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthorOrReadOnly]


@extend_schema(tags=["Lesson"])
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthorOrReadOnly]
