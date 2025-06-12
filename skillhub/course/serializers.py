from course.models import Category, Course, Lesson, Module
from django.db.models import Avg
from rest_framework import serializers
from review.models import Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
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
        avg = Review.objects.filter(course=obj).aggregate(avg_rating=Avg("rating"))[
            "avg_rating"
        ]
        return round(avg, 1) if avg else 0


class AnswerSerializer(serializers.Serializer):
    text = serializers.CharField()
    is_correct = serializers.BooleanField()


class QuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
    options = AnswerSerializer(many=True)


class QuizSerializer(serializers.Serializer):
    title = serializers.CharField()
    questions = QuestionSerializer(many=True)
