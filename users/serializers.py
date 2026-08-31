from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода данных об пользователе
    """

    class Meta:
        model = User
        fields = ("id", "first_name", "email", "avatar")
