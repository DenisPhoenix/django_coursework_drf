from django.contrib import admin

from habit.models import Habit, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Вывод локаций в админку"""

    list_display = ("name", "created_at")


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Вывод привычек в админку"""

    list_display = ("user", "location", "pleasant_habit", "completion_time", "publicity")
