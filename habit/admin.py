from django.contrib import admin

from habit.models import Habit, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Вывод локаций в админку"""

    list_display = ("name", "created_at")


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Вывод привычек в админку"""

    list_display = ("owner", "location", "is_pleasant", "completion_time", "is_published")
