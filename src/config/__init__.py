"""Конфигурация проекта. Загрузка токена из переменных окружения."""

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError(
        "TELEGRAM_TOKEN не найден! "
        "Добавьте переменную окружения в Railway или создайте .env файл."
    )
