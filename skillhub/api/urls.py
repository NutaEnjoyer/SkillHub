from django.urls import path, include 


urlpatterns = [
    path("users/", include("user.urls")),
    path("courses/", include("course.urls")),
    path("reviews/", include("review.urls")),
]
