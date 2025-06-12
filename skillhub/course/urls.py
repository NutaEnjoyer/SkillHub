from course import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"categories", views.CategoryViewSet)
router.register(r"courses", views.CourseViewSet)
router.register(r"modules", views.ModuleViewSet)
router.register(r"lessons", views.LessonViewSet)
router.register(r"quizzes", views.QuizViewSet)
router.register(r"questions", views.QuestionViewSet)
router.register(r"answers", views.AnswerViewSet)

urlpatterns = router.urls
