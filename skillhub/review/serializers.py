from course.models import Course
from rest_framework import serializers
from review.models import Review


class CourseShortSerializer(serializers.ModelSerializer):
    """
    Short serializer for courses.

    - `id`: The ID of the course.
    - `title`: The title of the course.
    """

    class Meta:
        model = Review
        fields = ["id", "title"]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review serializer for reviews.

    - `course_id`: The ID of the course for which the review is being created.
    - `user`: The user who created the review.
    - `rating`: The rating given to the course (1-5).
    - `title`: The title of the review.
    - `content`: The content of the review.
    """

    course = CourseShortSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source="course", write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
