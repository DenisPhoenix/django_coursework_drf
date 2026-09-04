from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwner(BasePermission):
    """Правило для проверки является ли пользователь владельцем объекта"""

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        user = request.user
        if user.is_authenticated:
            if obj.email == user.email:
                return True
        return False
