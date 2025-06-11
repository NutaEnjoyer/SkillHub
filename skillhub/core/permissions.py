from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ["instructor", "admin"]
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_authenticated and request.user.role == "student":
            return False

        if request.user.is_authenticated and request.user.role == "admin":
            return True

        course_author = self.get_course_author(obj)

        if not course_author:
            return False

        return bool(request.user.is_authenticated and course_author == request.user)

    def get_course_author(self, obj):
        try:
            if hasattr(obj, "course"):
                return obj.course.author
            if hasattr(obj, "module"):
                return obj.module.course.author
            if hasattr(obj, "lesson"):
                return obj.lesson.module.course.author
            if hasattr(obj, "quiz"):
                return obj.quiz.lesson.module.course.author
            if hasattr(obj, "question"):
                return obj.question.quiz.lesson.module.course.author
            if hasattr(obj, "answer"):
                return obj.answer.question.quiz.lesson.module.course.author
        except AttributeError:
            return None
