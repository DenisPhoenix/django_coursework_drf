from rest_framework import serializers

from habit.models import Habit, Location


class LocationSerializer(serializers.ModelSerializer):
    """Сериалайзер модели локаций"""

    class Meta:
        model = Location
        fields = ("id", "name", "address", "description", "created_at")


class OwnerAndPublishedHabitSerializer(serializers.ModelSerializer):
    """Сериалайзер модели привычки"""

    pleasant_habit = serializers.BooleanField(required=True)
    completion_time = serializers.IntegerField(required=True)

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "location",
            "time",
            "action",
            "pleasant_habit",
            "connection_habit",
            "periodicity",
            "remuneration",
            "completion_time",
            "publicity",
        )

    def validate(self, data):
        """Общая валидация полей привычки"""
        connection_habit = data.get("connection_habit")
        remuneration = data.get("remuneration")
        pleasant_habit = data.get("pleasant_habit")

        if connection_habit is not None and remuneration is not None:
            raise serializers.ValidationError("Нельзя одновременно заполнять вознаграждение и связанную привычку.")

        if not pleasant_habit and connection_habit is not None:
            raise serializers.ValidationError("Полезные привычки не могут быть связанными привычками")

        if connection_habit and not connection_habit.pleasant_habit:
            raise serializers.ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки."
            )

        return data


class NotOwnerHabitSerializer(serializers.ModelSerializer):
    """Сериалайзер модели привычки"""

    pleasant_habit = serializers.BooleanField(required=True)
    completion_time = serializers.IntegerField(required=True)

    class Meta:
        model = Habit
        fields = (
            "id",
            "action",
            "pleasant_habit",
            "completion_time",
            "publicity",
        )
