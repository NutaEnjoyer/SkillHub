from course.models import Answer, Category, Course, Lesson, Module, Question, Quiz
from course.serializers import CourseSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CourseSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="Test User",
        )
        self.category = Category.objects.create(name="Test Category")
        self.course = Course.objects.create(
            title="Test Course",
            description="This is a test course",
            category=self.category,
            author=self.user,
            level="beginner",
        )
        self.module = Module.objects.create(course=self.course, title="Test Module")
        self.lesson = Lesson.objects.create(module=self.module, title="Test Lesson")
        self.quiz = Quiz.objects.create(lesson=self.lesson)
        self.question = Question.objects.create(
            quiz=self.quiz, question_text="Test Question"
        )
        self.answer = Answer.objects.create(
            question=self.question, option_text="Test Answer", is_correct=True
        )

    def test_valid_data_serialization(self):
        data = {
            "title": "Test Course",
            "description": "This is a test course",
            "category": self.category.id,
            "author": self.user.id,
            "level": "beginner",
            "modules": [
                {
                    "title": "Test Module",
                    "lessons": [
                        {
                            "title": "Test Lesson",
                            "quizzes": [
                                {
                                    "questions": [
                                        {
                                            "text": "Test Question",
                                            "answers": [
                                                {
                                                    "text": "Test Answer",
                                                    "is_correct": True,
                                                }
                                            ],
                                        }
                                    ]
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        serializer = CourseSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["title"], "Test Course")
        self.assertEqual(
            serializer.validated_data["description"], "This is a test course"
        )
        self.assertEqual(serializer.validated_data["level"], "beginner")

    def test_invalid_data_serialization(self):
        data = {
            "title": "Test Course",
            "description": "This is a test course",
            "category": self.category.id,
            "author": self.user.id,
            "level": "invalid_level",
            "modules": [
                {
                    "title": "Test Module",
                    "lessons": [
                        {
                            "title": "Test Lesson",
                            "quizzes": [
                                {
                                    "questions": [
                                        {
                                            "text": "Test Question",
                                            "answers": [
                                                {
                                                    "text": "Test Answer",
                                                    "is_correct": True,
                                                }
                                            ],
                                        }
                                    ]
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        serializer = CourseSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("level", serializer.errors)
