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
    """
    Endpoint for managing categories.

    - GET /categories/: Retrieve a list of all categories.
    - POST /categories/: Create a new category.
    - GET /categories/{id}/: Retrieve a specific category by ID.
    - PUT/PATCH /categories/{id}/: Update a specific category by ID.
    - DELETE /categories/{id}/: Delete a specific category by ID.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=["Course"])
class CourseViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing courses.

    - GET /courses/: Retrieve a list of all courses.
    - POST /courses/: Create a new course.
    - GET /courses/{id}/: Retrieve a specific course by ID.
    - PUT/PATCH /courses/{id}/: Update a specific course by ID.
    - DELETE /courses/{id}/: Delete a specific course by ID.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Override the perform_create method to set the author field in the serializer.
        """

        serializer.save(author=self.request.user)


@extend_schema(tags=["Module"])
class ModuleViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing modules.

    - GET /modules/: Retrieve a list of all modules.
    - POST /modules/: Create a new module.
    - GET /modules/{id}/: Retrieve a specific module by ID.
    - PUT/PATCH /modules/{id}/: Update a specific module by ID.
    - DELETE /modules/{id}/: Delete a specific module by ID.
    """

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthorOrReadOnly]


@extend_schema(tags=["Lesson"])
class LessonViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing lessons.

    - GET /lessons/: Retrieve a list of all lessons.
    - POST /lessons/: Create a new lesson.
    - GET /lessons/{id}/: Retrieve a specific lesson by ID.
    - PUT/PATCH /lessons/{id}/: Update a specific lesson by ID.
    - DELETE /lessons/{id}/: Delete a specific lesson by ID.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Override the perform_create method to set the author field in the serializer and send a notification email.
        """

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
    """
    Endpoint for managing quizzes.

    - GET /quizzes/: Retrieve a list of all quizzes.
    - POST /quizzes/: Create a new quiz.
    - GET /quizzes/{id}/: Retrieve a specific quiz by ID.
    - PUT/PATCH /quizzes/{id}/: Update a specific quiz by ID.
    - DELETE /quizzes/{id}/: Delete a specific quiz by ID.
    """

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthorOrReadOnly]


@extend_schema(tags=["Question"])
class QuestionViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing questions.

    - GET /questions/: Retrieve a list of all questions.
    - POST /questions/: Create a new question.
    - GET /questions/{id}/: Retrieve a specific question by ID.
    - PUT/PATCH /questions/{id}/: Update a specific question by ID.
    - DELETE /questions/{id}/: Delete a specific question by ID.
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthorOrReadOnly]


@extend_schema(tags=["Answer"])
class AnswerViewSet(viewsets.ModelViewSet):
    """
    Endpoint for managing answers.

    - GET /answers/: Retrieve a list of all answers.
    - POST /answers/: Create a new answer.
    - GET /answers/{id}/: Retrieve a specific answer by ID.
    - PUT/PATCH /answers/{id}/: Update a specific answer by ID.
    - DELETE /answers/{id}/: Delete a specific answer by ID.
    """

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthorOrReadOnly]
