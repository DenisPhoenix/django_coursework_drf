# Курсовая работа. Проект 5. Трекер привычек

## Описание:

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и
искоренению старых плохих привычек. Этот проект содержит бэкенд-часть SPA веб-приложения трекера полезных привычек.

## Установка:

1. Установить основных зависимостей: "django", "celery", "redis", "psycopg2", "requests", "eventlet", "
   djangorestframework", "django-cors-headers", "python-dotenv", "pillow", "djangorestframework-simplejwt",
   "drf-spectacular", "django-celery-beat"

2. Установить дополнительных зависимостей: "flake8", "isort", "black", "mypy", "ipython", "django-stubs", "celery-types",
   "djangorestframework-stubs", "coverage"

3. Настройка зависимостей:

```
# pyproject.toml
[tool.black]
line-length = 119
target-version = ['py314']
exclude = '''
/(
    \.git
  | __pycache__
  | env
  | venv
  | \.venv
  | migrations
)/
'''

[tool.isort]
line_length = 119

[tool.mypy]
disallow_untyped_defs = true
warn_return_any = true
exclude = "venv"
plugins = [
    "mypy_django_plugin.main"
]

[[tool.mypy.overrides]]
module = "django_celery_beat.*"
ignore_missing_imports = true

[tool.django-stubs]
django_settings_module = "config.settings"
strict_model_abstract_attrs = false
strict_settings_type = false

[tool.coverage.run]
source = ["."]               # Директории для анализа (корень проекта)
omit = [
    "*/migrations/*",        # Игнорировать миграции Django
    "*/settings.py",         # Игнорировать файл настроек
    "*/wsgi.py",
    "*/asgi.py",
    "manage.py",
    "*/tests/*",             # Сами тесты обычно исключают из отчета
]
```

## Структура проекта

+ `config/`: Настройки проекта
+ `habit/`: Приложение Привычки
+ `users/`: Приложение Пользователей
+ `manage.py`: Запуска команд Django
+ `.env_example`: Пример переменных окружения
+ `.gitignore`: Игнорируемые файлы для Git
+ `pyproject.toml`: Файл c зависимостями проекта
+ `.flake8`: Настройки линтера flake8
+ `README.md`: Описание проекта