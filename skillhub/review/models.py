from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator



class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    created_at = models.DateField(auto_now=True)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name="reviews")


    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ('-created_at',)

    
    def __str__(self):
        return f"{self.title} (f{self.rating}/5)"
    