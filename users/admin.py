from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Вывод модели пользователя в админку"""

    list_display = ("email", "last_login", "date_joined")
    readonly_fields = ("password", "last_login", "date_joined")
    fieldsets = [
        (
            "Личная информация",
            {"fields": ("first_name", "last_name", "username")},
        ),
        ("Контактная информация", {"fields": ("email",)}),
        (
            "Права",
            {
                "fields": ("is_superuser", "is_active", "groups", "user_permissions", "password"),
                "classes": ("collapse",),
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined"), "classes": ("collapse",)}),
    ]
