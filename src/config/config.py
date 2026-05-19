"""Конфигурация проекта. Загружает токен из переменных окружения."""

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла (если он есть)
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError(
        "TELEGRAM_TOKEN не найден! "
        "Создайте файл .env или добавьте переменную окружения."
    )
