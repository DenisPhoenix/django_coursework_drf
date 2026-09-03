from rest_framework import serializers


def habit_select_together_validator(related_habit, reward):
    """Проверка одновременного заполнения полей"""
    if related_habit is not None and reward is not None:
        raise serializers.ValidationError("Нельзя одновременно заполнять вознаграждение и связанную привычку.")


def habit_is_pleasant_have_remuneration(is_pleasant, related_habit, reward):
    """Проверка есть ли у приятной привычки вознаграждение и связанная привычка"""
    if (
        is_pleasant
        and (related_habit is not None and reward is not None)
        or (related_habit is None and reward is None)
    ):
        raise serializers.ValidationError("У приятной привычки не может быть вознаграждения и связанной привычки.")


def habit_is_pleasant(related_habit):
    """Проверка является ли привычка полезной для связанной привычки"""
    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )
