from course.models import Answer, Category, Course, Lesson, Module, Question, Quiz
from django.db.models import Avg
from rest_framework import serializers
from review.models import Review


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer for categories.
    """

    class Meta:
        model = Category
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """
    Lesson serializer for lessons.
    """

    class Meta:
        model = Lesson
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    """
    Module serializer for modules.
    """

    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Course serializer for courses.

    - `id`: The ID of the course.
    - `title`: The title of the course.
    - `description`: The description of the course.
    - `author`: The author of the course.
    - `category`: The category of the course.
    - `level`: The level of the course.
    - `modules`: The modules of the course.
    - `created_at`: The date when the course was created.
    - `updated_at`: The date when the course was last updated.
    - `avg_rate`: The average rating of the course.
    """

    modules = ModuleSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.StringRelatedField(read_only=True)
    avg_rate = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "author",
            "category",
            "level",
            "modules",
            "created_at",
            "updated_at",
            "avg_rate",
        ]
        read_only_fields = ["author", "students", "created_at", "updated_at"]

    def get_avg_rate(self, obj):
        """
        Aggregate the average rating for the course.
        """

        avg = Review.objects.filter(course=obj).aggregate(avg_rating=Avg("rating"))[
            "avg_rating"
        ]
        return round(avg, 1) if avg else 0


class AnswerSerializer(serializers.ModelSerializer):
    """
    Answer serializer for quiz questions.

    - `text`: The text of the answer.
    - `is_correct`: Indicates whether the answer is correct.
    """

    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    text = serializers.CharField()
    is_correct = serializers.BooleanField()

    class Meta:
        model = Answer
        fields = ["question", "text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question serializer for quiz questions.

    - `text`: The text of the question.
    - `options`: The options for the question.
    """

    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
    text = serializers.CharField()
    options = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ["quiz", "question_text", "options"]


class QuizSerializer(serializers.ModelSerializer):
    """
    Quiz serializer for quizzes.

    - `lesson`: The lesson associated with the quiz.
    - `title`: The title of the quiz.
    - `questions`: The questions in the quiz.
    """

    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    title = serializers.CharField()
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Quiz
        fields = ["lesson", "title", "questions"]
