from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsOwner
from users.serializers import NotOwnerUserSerializer, OwnerUserSerializer


class UserViewSet(ModelViewSet):
    """Вьюсет пользователя"""

    queryset = User.objects.all()

    def get_permissions(self):
        """
        Метод для получения разрешения в зависимости от метода
        """
        if self.action == "create":
            return (AllowAny(),)
        elif self.action in ("update", "partial_update", "destroy", "retrieve"):
            return (IsOwner(),)
        return super().get_permissions()

    def get_serializer_class(self):
        """Метод для получения сериалайзера в зависимости от метода"""
        if getattr(self, "swagger_fake_view", False):
            return NotOwnerUserSerializer

        if self.action == "list":
            return NotOwnerUserSerializer
        if self.action in ("update", "partial_update", "create", "retrieve"):
            return OwnerUserSerializer

    def retrieve(self, request, *args, **kwargs):
        """Метод для выдачи сериалайзера в зависимости от владения профилем"""
        instance = self.get_object()

        if instance.email == request.user.email:
            serializer = OwnerUserSerializer(instance)
        else:
            serializer = NotOwnerUserSerializer(instance)

        return Response(serializer.data)

    def perform_create(self, serializer):
        """Метод для создания пользователя"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
        return

    def perform_update(self, serializer):
        """Метод для обновления пользователя"""
        password = serializer.validated_data.pop("password", None)
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
