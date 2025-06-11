from rest_framework.routers import DefaultRouter
from course import views    


router = DefaultRouter()

router.register(r'categories', views.CategoryViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'lessons', views.LessonViewSet)

urlpatterns = router.urls
