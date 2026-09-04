from rest_framework import serializers

from habit.models import Habit, Location
from habit.validators import habit_is_pleasant, habit_is_pleasant_have_remuneration, habit_select_together_validator


class LocationSerializer(serializers.ModelSerializer):
    """Сериалайзер модели локаций"""

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Location
        fields = ("id", "name", "address", "description", "created_at")


class OwnerHabitSerializer(serializers.ModelSerializer):
    """Сериалайзер модели привычки"""

    is_pleasant = serializers.BooleanField(required=True)
    completion_time = serializers.IntegerField()

    class Meta:
        model = Habit
        fields = (
            "id",
            "owner",
            "location",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "period",
            "reward",
            "completion_time",
            "is_published",
        )

    def validate(self, data: dict) -> dict:
        """Общая валидация полей привычки"""
        request = self.context.get("request")
        if request and request.method == "POST":
            related_habit = data.get("related_habit")
            reward = data.get("reward")
            is_pleasant = data.get("is_pleasant")

            habit_select_together_validator(related_habit, reward)
            habit_is_pleasant_have_remuneration(is_pleasant, related_habit, reward)
            habit_is_pleasant(related_habit)

        return data

    def validate_completion_time(self, value: int) -> int:
        """Валидации выполнения привычки"""
        if value > 120:
            raise serializers.ValidationError("Время выполнения не может быть больше 2 минут")
        elif value < 0:
            raise serializers.ValidationError("Время выполнения не может быть меньше 0 секунд")
        return value


class PublishedHabitSerializer(serializers.ModelSerializer):
    """Сериалайзер модели привычки"""

    is_pleasant = serializers.BooleanField(required=True)
    completion_time = serializers.IntegerField(required=True)

    class Meta:
        model = Habit
        fields = (
            "id",
            "action",
            "is_pleasant",
            "completion_time",
            "is_published",
        )
