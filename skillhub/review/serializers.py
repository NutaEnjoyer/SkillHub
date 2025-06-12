from course.models import Course
from rest_framework import serializers
from review.models import Review


class CourseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "title"]


class ReviewSerializer(serializers.ModelSerializer):
    course = CourseShortSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source="course", write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
