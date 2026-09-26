import re

from rest_framework import serializers

from users.models import User


class NotOwnerUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода данных об пользователе не являющимся владельцем"""

    class Meta:
        model = User
        fields = ("id", "first_name", "email")


class OwnerUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода данных об пользователе владельцу"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password", "tg_chat_id")

    def validate_email(self, value: str) -> str:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, value):
            raise serializers.ValidationError("Электронная почта введена не верно")

        return value
