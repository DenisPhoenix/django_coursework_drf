from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Правило для проверки является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email
