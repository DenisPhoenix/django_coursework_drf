from rest_framework import serializers


def habit_select_together_validator(related_habit, reward):
    if related_habit is not None and reward is not None:
        raise serializers.ValidationError("Нельзя одновременно заполнять вознаграждение и связанную привычку.")


def habit_is_connection_habit(related_habit, is_pleasant):
    if not is_pleasant and related_habit is not None:
        raise serializers.ValidationError("Полезные привычки не могут быть связанными привычками")


def habit_is_pleasant(related_habit):
    if related_habit and not related_habit.pleasant_habit:
        raise serializers.ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )
