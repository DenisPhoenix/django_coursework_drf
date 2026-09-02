from rest_framework import serializers

from users.models import User


class NotOwnerUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода данных об пользователе не являющимся владельцем"""

    class Meta:
        model = User
        fields = ("id", "first_name", "email")


class OwnerUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода данных об пользователе владельцу"""

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password")
