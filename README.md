# Курсовая работа. Проект 5. Трекер привычек

## Описание:

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и
искоренению старых плохих привычек. Этот проект содержит бэкенд-часть SPA веб-приложения трекера полезных привычек.

## Установка:

1. Установить основных зависимостей: "django", "celery", "redis", "psycopg2", "eventlet", "
   djangorestframework", "python-dotenv", "pillow", "djangorestframework-simplejwt",
   "drf-spectacular", "django-celery-beat"

2. Установить дополнительных зависимостей: "flake8", "isort", "black", "ipython", "django-stubs", "celery-types",
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

[tool.django-stubs]
django_settings_module = "config.settings"
strict_model_abstract_attrs = false
strict_settings_type = false
```

## Структура проекта

+ `config/`: Настройки проекта
+ `users/`: Приложение Пользователей
+ `manage.py`: Запуска команд Django
+ `.env_example`: Пример переменных окружения
+ `.gitignore`: Игнорируемые файлы для Git
+ `pyproject.toml`: Файл c зависимостями проекта
+ `.flake8`: Настройки линтера flake8