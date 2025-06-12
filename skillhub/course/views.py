from core.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from course.models import Answer, Category, Course, Lesson, Module, Question, Quiz
from course.serializers import (
    AnswerSerializer,
    CategorySerializer,
    CourseSerializer,
    LessonSerializer,
    ModuleSerializer,
    QuestionSerializer,
    QuizSerializer,
)
from drf_spectacular.utils import extend_schema
from notification.models import Notification
from notification.tasks import send_notification_email
from rest_framework import viewsets


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

    def perform_create(self, serializer):
        lesson = serializer.save()

        students = lesson.module.course.students.all()
        for student in students:
            notification = Notification.objects.create(
                user=student,
                message=f"New lesson {lesson.title} added to course {lesson.module.course.title}",
            )
            send_notification_email.delay(notification.id)


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
