# ==========================================
# Этап 1: Сборка зависимостей (Builder)
# ==========================================
FROM python:3.14-slim AS builder

WORKDIR /app

# Устанавливаем только необходимые для компиляции системные пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry и плагин экспорта
RUN pip install --no-cache-dir poetry poetry-plugin-export

# Копируем файлы зависимостей отдельно для эффективного кэширования
COPY pyproject.toml poetry.lock ./

# Экспортируем зависимости в requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Собираем wheel-пакеты во временную директорию
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# ==========================================
# Этап 2: Финальный образ (Runner)
# ==========================================
FROM python:3.14-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Копируем и устанавливаем скомпилированные зависимости
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* \
    && rm -rf /wheels

# Создаем необходимые пустые директории
RUN mkdir -p /app/media /app/static

# Копируем ТОЛЬКО исходный код приложения (исключая мусор)
COPY . /app

EXPOSE 8000