from notification.views import NotificationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"notifications", NotificationViewSet, basename="notification")

urlpatterns = [
    *router.urls,
]
