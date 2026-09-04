from typing import Any

import requests

from config import settings


def send_telegram_message(chat_id: str, message: str) -> Any:
    """Функция для отправки сообщений в телеграм"""
    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        response = requests.post(url, json=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
        return None
