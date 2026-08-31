from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(max_length=50, unique=True, verbose_name="Электронная почта")
    username = models.CharField(
        max_length=50,
        unique=False,
        blank=True,
        null=True,
        verbose_name="Имя пользователя",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
