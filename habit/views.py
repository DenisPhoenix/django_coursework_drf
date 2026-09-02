from django.db.models import Q
from rest_framework import permissions, viewsets

from habit.models import Habit, Location
from habit.pagination import HabitPaginator
from habit.permissions import IsOwner
from habit.serializers import LocationSerializer, NotOwnerHabitSerializer, OwnerAndPublishedHabitSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """Вьюсет для локаций"""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """Вьюсет для привычки"""

    pagination_class = HabitPaginator

    def get_permissions(self):
        """Метод для получения разрешения в зависимости от метода"""
        action = self.action
        if action in ("destroy", "update", "partial_update"):
            return (permissions.IsAuthenticated(), IsOwner())
        return super().get_permissions()

    def get_queryset(self):
        """Получение публичных и текущего пользователя объектов"""
        user = self.request.user

        if not user.is_authenticated:
            return Habit.objects.filter(publicity=True)

        return Habit.objects.filter(Q(user=user) | Q(publicity=True))

    def get_serializer_class(self):
        """Метод для получения сериалайзера в зависимости от метода"""
        if getattr(self, "swagger_fake_view", False):
            return NotOwnerHabitSerializer

        if self.action == "list":
            return NotOwnerHabitSerializer
        if self.action in ("update", "partial_update", "create", "retrieve"):
            return OwnerAndPublishedHabitSerializer

    def perform_create(self, serializer):
        """Метод для установки владельца по умолчанию"""
        serializer.save(user=self.request.user)
