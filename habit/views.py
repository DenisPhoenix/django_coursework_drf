from typing import Any, Sequence, Type

from django.db.models import QuerySet
from rest_framework import permissions, serializers, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.serializers import BaseSerializer

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

    def get_permissions(self) -> Sequence[Any]:
        """Метод для получения разрешения в зависимости от метода"""
        if self.action in ("destroy", "update", "partial_update"):
            return (
                permissions.IsAuthenticated(),
                IsOwner(),
            )
        return super().get_permissions()

    def get_queryset(self) -> QuerySet[Habit]:
        """Получение объектов текущего пользователя"""
        user = self.request.user
        if user.is_authenticated:
            queryset = Habit.objects.filter(owner=user)
        else:
            queryset = Habit.objects.none()
        return queryset

    def get_serializer_class(self) -> Type[BaseSerializer]:
        """Метод для получения сериалайзера в зависимости от метода"""
        action = self.action

        if getattr(self, "swagger_fake_view", False):
            return OwnerHabitSerializer

        if action == "list":
            return PublishedHabitSerializer
        elif action in ("update", "create", "partial_update", "retrieve"):
            return OwnerHabitSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer: serializers.BaseSerializer) -> None:
        """Метод для установки владельца по умолчанию"""
        serializer.save(owner=self.request.user)


class PublishedHabit(ListAPIView):
    """Вьюха для списка публичных привычек"""

    serializer_class = PublishedHabitSerializer

    def get_queryset(self) -> QuerySet[Habit]:
        """Выбор публичных привычек"""
        return Habit.objects.filter(is_published=True)
