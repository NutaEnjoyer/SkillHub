from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


    class Meta: 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_courses',
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_courses',
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta: 
        ordering = ['-created_at']
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self):
        return f"{self.title} (Course: {self.course.title})"
    
    def save(self, *args, **kwargs):
        if self._state.adding and self.order == 0:
            last_order = Module.objects.filter(course=self.course).order_by("-order").first()
            self.order = last_order.order + 1 if last_order else 1
        super().save(*args, **kwargs)


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='lesson/pdfs/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta: 
        ordering = ['order']
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return f"{self.title} (Module: {self.module.title}) (Course: {self.module.course.title})"
    
    def save(self, *args, **kwargs):
        if self._state.adding and self.order == 0:
            last_order = Lesson.objects.filter(module=self.module).order_by('-order').first()
            self.order = last_order.order + 1 if last_order else 1
        super().save(*args, **kwargs)
