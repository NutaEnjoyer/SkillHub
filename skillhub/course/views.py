from rest_framework import viewsets, permissions
from course.models import Category, Course, Module, Lesson, Quiz, Question, Answer
from course.serializers import (
    CategorySerializer,
    CourseSerializer,
    ModuleSerializer,
    LessonSerializer,
    QuestionSerializer,
    AnswerSerializer,
    QuizSerializer,
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


@extend_schema(tags=["Quiz"])
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthorOrReadOnly]


@extend_schema(tags=["Question"])
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthorOrReadOnly]


@extend_schema(tags=["Answer"])
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthorOrReadOnly]
