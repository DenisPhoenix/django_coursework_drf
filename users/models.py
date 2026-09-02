from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    email = models.CharField(max_length=50, unique=True, verbose_name="Электронная почта")
    username = models.CharField(max_length=50, unique=False, blank=True, null=True, verbose_name="Имя пользователя")
    tg_chat_id = models.CharField(max_length=15, blank=True, null=True, verbose_name="Chat ID")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
