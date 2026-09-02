from rest_framework import serializers

from habit.models import Habit, Location
from habit.validators import habit_is_connection_habit, habit_is_pleasant, habit_select_together_validator


class LocationSerializer(serializers.ModelSerializer):
    """Сериалайзер модели локаций"""

    class Meta:
        model = Location
        fields = ("id", "name", "address", "description", "created_at")


class OwnerHabitSerializer(serializers.ModelSerializer):
    """Сериалайзер модели привычки"""

    is_pleasant = serializers.BooleanField(required=True)

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

    def validate(self, data):
        """Общая валидация полей привычки"""
        related_habit = data.get("related_habit")
        reward = data.get("reward")
        is_pleasant = data.get("is_pleasant")

        habit_select_together_validator(related_habit, reward)
        habit_is_connection_habit(related_habit, is_pleasant)
        habit_is_pleasant(related_habit)

        return data


class PublishedHabitSerializer(serializers.ModelSerializer):
    """Сериалайзер модели привычки"""

    is_pleasant = serializers.BooleanField(required=True)
    completion_time = serializers.IntegerField(required=True)

    class Meta:
        model = Habit
        fields = (
            "id",
            "action",
            "related_habit",
            "completion_time",
            "is_published",
        )
