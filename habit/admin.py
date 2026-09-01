from django.contrib import admin

from habit.models import Habit, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "pleasant_habit", "completion_time", "publicity")
