from course import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"courses", views.CourseViewSet, basename="course")
router.register(r"modules", views.ModuleViewSet, basename="module")
router.register(r"lessons", views.LessonViewSet, basename="lesson")
router.register(r"quizzes", views.QuizViewSet, basename="quiz")
router.register(r"questions", views.QuestionViewSet, basename="question")
router.register(r"answers", views.AnswerViewSet, basename="answer")

urlpatterns = router.urls
