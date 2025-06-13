from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Category model for courses.

    - `name`: The name of the category.
    - `description`: The description of the category.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Course model for skillhub.

    - `author`: The user who created the course.
    - `title`: The title of the course.
    - `description`: The description of the course.
    - `category`: The category to which the course belongs.
    - `level`: The level of the course (beginner, intermediate, advanced).
    - `students`: The list of students enrolled in the course.
    - `created_at`: The date when the course was created.
    """

    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_courses",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="enrolled_courses",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title


class Module(models.Model):
    """
    Module model for courses.

    - `course`: The course to which the module belongs.
    - `title`: The title of the module.
    - `description`: The description of the module.
    - `order`: The order of the module in the course.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self):
        return f"{self.title} (Course: {self.course.title})"

    def save(self, *args, **kwargs):
        """
        Override the save method to set the order based on the previous module's order.
        """

        if self._state.adding and self.order == 0:
            last_order = (
                Module.objects.filter(course=self.course).order_by("-order").first()
            )
            self.order = last_order.order + 1 if last_order else 1
        super().save(*args, **kwargs)


class Lesson(models.Model):
    """
    Lsson model for courses.

    - `module`: The module to which the lesson belongs.
    - `title`: The title of the lesson.
    - `content`: The content of the lesson.
    - `video_url`: The URL of the video for the lesson.
    - `pdf_file`: The PDF file for the lesson.
    - `order`: The order of the lesson in the module.
    """

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to="lesson/pdfs/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return f"{self.title} (Module: {self.module.title}) (Course: {self.module.course.title})"

    def save(self, *args, **kwargs):
        """
        Override the save method to set the order based on the previous lesson's order.
        """

        if self._state.adding and self.order == 0:
            last_order = (
                Lesson.objects.filter(module=self.module).order_by("-order").first()
            )
            self.order = last_order.order + 1 if last_order else 1
        super().save(*args, **kwargs)


class Quiz(models.Model):
    """
    Quiz model for lessons.

    - `lesson`: The lesson to which the quiz belongs.
    - `title`: The title of the quiz.
    """

    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name="quiz")
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizs"

    def __str__(self):
        return f"{self.title} (Lesson: {self.lesson.title})"


class Question(models.Model):
    """
    Question model for quizzes.

    - `quiz`: The quiz to which the question belongs.
    - `question_text`: The text of the question.
    """

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()

    class Meta:
        verbose_name = "Quiz Answer"
        verbose_name_plural = "Quiz Answers"

    def __str__(self):
        return f"{self.question_text[:30]}"


class Answer(models.Model):
    """
    Answer model for questions.

    - `question`: The question to which the answer belongs.
    - `option_text`: The text of the answer option.
    - `is_correct`: Whether the answer is correct or not.
    """

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Quiz Answer Option"
        verbose_name_plural = "Quiz Answer Options"

    def __str__(self):
        return f"{self.option_text[:30]} (Correct: {self.is_correct})"
