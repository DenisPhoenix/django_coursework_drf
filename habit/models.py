from django.core.validators import MaxValueValidator
from django.db import models


class Location(models.Model):
    """Модель локаций"""

    name = models.CharField(max_length=200, verbose_name="Название")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Адрес")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Habit(models.Model):
    """Модель привычки"""

    HABIT_PERIODICITY = [
        ("daily", "ежедневная"),
        ("two_days", "2 дня"),
        ("three_days", "3 дня"),
        ("four_days", "4 дня"),
        ("five_days", "5 дней"),
        ("six_days", "6 дней"),
        ("weekly", "еженедельно"),
    ]

    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь"
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=150, verbose_name="Действие привычки")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Связанная привычка"
    )
    period = models.CharField(max_length=12, choices=HABIT_PERIODICITY, default="daily", verbose_name="Периодичность")
    reward = models.CharField(max_length=250, null=True, blank=True, verbose_name="Вознаграждение")
    completion_time = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)], verbose_name="Время на выполнение"
    )
    is_published = models.BooleanField(default=False, verbose_name="Признак публичности")

    def __str__(self):
        return f"я буду {self.action} в {self.time} в {self.location}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("-time",)
