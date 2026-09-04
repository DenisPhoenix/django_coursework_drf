from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView

from habit.models import Habit, Location
from habit.pagination import HabitPaginator
from habit.permissions import IsOwner
from habit.serializers import LocationSerializer, OwnerHabitSerializer, PublishedHabitSerializer


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
        """Получение объектов текущего пользователя"""
        return Habit.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        """Метод для получения сериалайзера в зависимости от метода"""
        if getattr(self, "swagger_fake_view", False):
            return OwnerHabitSerializer

        if self.action == "list":
            return PublishedHabitSerializer
        elif self.action in ("update", "partial_update", "create", "retrieve"):
            return OwnerHabitSerializer

    def perform_create(self, serializer):
        """Метод для установки владельца по умолчанию"""
        serializer.save(owner=self.request.user)


class PublishedHabit(ListAPIView):
    """Вьюха для списка публичных привычек"""

    serializer_class = PublishedHabitSerializer

    def get_queryset(self):
        """Выбор публичных привычек"""
        return Habit.objects.filter(publicity=True)
