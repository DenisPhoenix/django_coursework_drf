from typing import Any, Sequence, Type

from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsOwner
from users.serializers import NotOwnerUserSerializer, OwnerUserSerializer


class UserViewSet(ModelViewSet):
    """Вьюсет пользователя"""

    queryset = User.objects.all()

    def get_permissions(self) -> Sequence[Any]:
        """
        Метод для получения разрешения в зависимости от метода
        """
        if self.action == "create":
            return (AllowAny(),)
        elif self.action in ("update", "partial_update", "destroy", "retrieve"):
            return (IsOwner(),)
        return super().get_permissions()

    def get_serializer_class(self) -> Type[BaseSerializer]:
        """Метод для получения сериалайзера в зависимости от метода"""
        if getattr(self, "swagger_fake_view", False):
            return NotOwnerUserSerializer

        if self.action == "list":
            return NotOwnerUserSerializer
        if self.action in ("update", "partial_update", "create", "retrieve"):
            return OwnerUserSerializer

        return super().get_serializer_class()

    def retrieve(self, request: Request, *args: list, **kwargs: dict) -> Response:
        """Метод для выдачи сериалайзера в зависимости от владения профилем"""
        instance = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response({"detail": "Учетные данные не были предоставлены."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer: BaseSerializer
        if instance.email == user.email:
            serializer = OwnerUserSerializer(instance)
        else:
            serializer = NotOwnerUserSerializer(instance)

        return Response(serializer.data)

    def perform_create(self, serializer: serializers.BaseSerializer) -> None:
        """Метод для создания пользователя"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer: serializers.BaseSerializer) -> None:
        """Метод для обновления пользователя"""
        password = serializer.validated_data.pop("password", None)
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
