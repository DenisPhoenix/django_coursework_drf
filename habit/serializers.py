from rest_framework import serializers

from habit.models import Habit, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("name", "address", "description", "created_at")


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            "user",
            "location",
            "time",
            "action",
            "pleasant_habit",
            "linked_habit",
            "periodicity",
            "remuneration",
            "completion_time",
            "publicity",
        )
