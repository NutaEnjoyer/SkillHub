from course.models import Answer, Category, Course, Lesson, Module, Question, Quiz
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class Base(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strong_password_12",
            full_name="Test User",
            role="admin",
        )
        self.category = Category.objects.create(name="Test Category")

        self.course_data = {
            "title": "Test Course",
            "description": "This is a test course",
            "category": self.category.id,
            "author": self.user.id,
            "level": "beginner",
        }

        self.module_data = {
            "title": "Test Module",
            "description": "This is a test module",
        }

        self.lesson_data = {
            "title": "Test Lesson",
            "content": "Test content",
        }

        self.quiz_data = {
            "title": "Test Quiz",
        }

        self.question_data = {
            "question_text": "Test question",
        }

        self.answer_data = {
            "option_text": "Test option",
            "is_correct": True,
        }

    def test_create_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("course-list")
        response = self.client.post(url, self.course_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.last().title, "Test Course")
        self.assertEqual(Course.objects.last().description, "This is a test course")
        self.assertEqual(Course.objects.last().category, self.category)
        self.assertEqual(Course.objects.last().author, self.user)
        self.assertEqual(Course.objects.last().level, "beginner")
        self.assertEqual(Course.objects.last().students.count(), 0)

    def test_invalid_data_create_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("course-list")
        data = {
            "title": "Test Course",
            "description": "This is a test course",
            "category": self.category.id,
            "author": self.user.id,
            "level": "invalid_level",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 0)
        self.assertIn("level", response.data)

    def test_unauthenticated_create_course(self):
        url = reverse("course-list")
        response = self.client.post(url, self.course_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Course.objects.count(), 0)

    def test_get_course_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("course-list")
        response = self.client.post(url, self.course_data, format="json")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_module(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("course-list")
        response = self.client.post(url, self.course_data, format="json")

        course = Course.objects.last()

        data = self.module_data
        data["course"] = course.id

        url = reverse("module-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 1)

    def test_create_lesson(self):
        course = Course.objects.create(
            author=self.user,
            category=self.category,
            **{
                k: v
                for k, v in self.course_data.items()
                if k not in ["author", "category"]
            }
        )

        module = Module.objects.create(course=course, **self.module_data)

        data = {"module": module.id, **self.lesson_data}

        self.client.force_authenticate(user=self.user)
        url = reverse("lesson-list")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.last().title, "Test Lesson")
        self.assertEqual(Lesson.objects.last().content, "Test content")
        self.assertEqual(Lesson.objects.last().module, module)

    def test_create_quiz(self):
        course = Course.objects.create(
            author=self.user,
            category=self.category,
            **{
                k: v
                for k, v in self.course_data.items()
                if k not in ["author", "category"]
            }
        )

        module = Module.objects.create(course=course, **self.module_data)

        lesson = Lesson.objects.create(module=module, **self.lesson_data)

        data = {"lesson": lesson.id, **self.quiz_data}

        self.client.force_authenticate(user=self.user)
        url = reverse("quiz-list")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(Quiz.objects.last().lesson, lesson)

    def test_create_question(self):
        course = Course.objects.create(
            author=self.user,
            category=self.category,
            **{
                k: v
                for k, v in self.course_data.items()
                if k not in ["author", "category"]
            }
        )

        module = Module.objects.create(course=course, **self.module_data)

        lesson = Lesson.objects.create(module=module, **self.lesson_data)

        quiz = Quiz.objects.create(lesson=lesson, **self.quiz_data)

        data = {"quiz": quiz.id, **self.question_data}

        self.client.force_authenticate(user=self.user)
        url = reverse("question-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

    def test_create_answer(self):
        course = Course.objects.create(
            author=self.user,
            category=self.category,
            **{
                k: v
                for k, v in self.course_data.items()
                if k not in ["author", "category"]
            }
        )

        module = Module.objects.create(course=course, **self.module_data)

        lesson = Lesson.objects.create(module=module, **self.lesson_data)

        quiz = Quiz.objects.create(lesson=lesson, **self.quiz_data)

        question = Question.objects.create(quiz=quiz, **self.question_data)

        data = {"question": question.id, **self.answer_data}

        self.client.force_authenticate(user=self.user)
        url = reverse("answer-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.last().option_text, "Test option")
        self.assertTrue(Answer.objects.last().is_correct)
