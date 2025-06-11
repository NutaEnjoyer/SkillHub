from rest_framework.routers import DefaultRouter
from review import views

router = DefaultRouter()

router.register(r"reviews", views.ReviewViewSet, basename="review")


urlpatterns = [
    *router.urls,
]
