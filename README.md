# Курсовая работа. Проект 5. Трекер привычек

## Описание:

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и
искоренению старых плохих привычек. Этот проект содержит бэкенд-часть SPA веб-приложения трекера полезных привычек.

## Зависимости и инструменты:

1. Установить основных зависимостей: "django", "celery", "redis", "psycopg2", "requests", "eventlet", "
   djangorestframework", "django-cors-headers", "python-dotenv", "pillow", "djangorestframework-simplejwt",
   "drf-spectacular", "django-celery-beat"

2. Установить дополнительных зависимостей: "flake8", "isort", "black", "mypy", "ipython", "django-stubs", "celery-types",
   "djangorestframework-stubs", "coverage"

3. Настройка инструментов (pyproject.toml):

```
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

## Запуск проекта

### Локальный запуск (через Docker)

> **Перед началом:** Убедитесь, что у вас установлен и запущен [Docker Desktop](https://docker.com).

Выполните следующие шаги в терминале:

1. **Клонируйте репозиторий** и перейдите в корневую директорию проекта:
   ```bash
   git clone <ссылка_на_ваш_репозиторий>
   cd <название_папки_проекта>
   ```

2. **Настройте переменные окружения.** Создайте файл конфигурации из шаблона и при необходимости отредактируйте его:
   ```bash
   cp .env.template .env
   ```
   *(Для Windows PowerShell используйте: `copy .env.template .env`)*

3. **Соберите и запустите** Docker-контейнеры в фоновом режиме:
   ```bash
   docker compose up -d --build
   ```


### Доступ к приложению

После успешной сборки и запуска контейнеров проект будет доступен по адресам:

* **Основной сайт:** [http://localhost:8000](http://localhost:8000)
* **Панель администратора:** [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Запуск на сервере & CI/CD

Автоматический деплой проекта реализован с помощью **GitHub Actions** и **Docker Hub**. При каждом пуше в ветку `main` проект автоматически собирается и обновляется на сервере.

### Шаг 1. Настройка секретов в GitHub

Перед запуском пайплайна необходимо передать учетные данные для доступа к серверу и реестру контейнеров.

1. Перейдите в ваш репозиторий на **GitHub**.
2. Откройте **Settings** ➔ **Secrets and variables** ➔ **Actions**.
3. Нажмите кнопку **New repository secret** и поочередно добавьте следующие переменные:

| Ключ секретирования (Secret) | Что туда вставлять |
| :--- | :--- |
| `DOCKER_HUB_USERNAME` | Ваше имя пользователя (логин) на Docker Hub. |
| `DOCKER_HUB_ACCESS_TOKEN` | Сгенерированный токен доступа (Personal Access Token) из Docker Hub. |
| `SSH_KEY` | Ваш приватный SSH-ключ для подключения к серверу. |
| `SSH_USER` | Имя пользователя на сервере (например, `root` или `ubuntu`). |
| `SERVER_IP` | Публичный IP-адрес вашего удаленного сервера. |

> ⚠️ **Важно:** Ни в коем случае не публикуйте эти данные в открытом виде внутри кода!

---

### Автоматический деплой (CI/CD)

### Как устроен рабочий процесс:
1. Вы вносите изменения в код локально.
2. Фиксируете их: `git commit -m "feat: добавлена новая функция"`.
3. Отправляете код в удаленный репозиторий: `git push origin main`.
4. **GitHub Actions** автоматически подхватывает изменения:
   * Собирает новый Docker-образ вашего Django-приложения.
   * Отправляет (push) его в ваш приватный/публичный репозиторий на **Docker Hub**.
   * Подключается к серверу по SSH, скачивает (pull) свежий образ и перезапускает контейнеры.
   * Автоматически применяет новые миграции БД и собирает статические файлы.

Статус деплоя и подробные логи сборки всегда можно отслеживать во вкладке **Actions** вашего GitHub-репозитория.

## Структура проекта
+ `.github/`: GitHub Actions
+ `config/`: Настройки проекта
+ `deploy/`: Настойки деплоя
+ `habit/`: Приложение Привычки
+ `nginx/`: Настройки Nginx
+ `users/`: Приложение Пользователей
+ `manage.py`: Запуска команд Django
+ `Dockerfile`: Файл для сборки образов
+ `docker-compose.yml`: Файл для настройки многоконтейнерных приложений
+ `.env_example`: Пример переменных окружения
+ `.gitignore`: Игнорируемые файлы для Git
+ `poetry.lock`: Файл с точными зависимостями проекта
+ `pyproject.toml`: Файл с зависимостями проекта
+ `.flake8`: Настройки линтера flake8
+ `README.md`: Описание проекта