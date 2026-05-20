"""Функции для работы с базой данных SQLite."""

import sqlite3
import pandas as pd

conn = sqlite3.connect("recsys.db", check_same_thread=False)
cursor = conn.cursor()


def init_db() -> None:
    """Создаёт таблицу взаимодействий, если она не существует."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            user_id INTEGER,
            item_id INTEGER,
            event TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def add_interaction_db(user_id: int, item_id: int, event: str) -> None:
    """Добавляет запись о взаимодействии пользователя."""
    cursor.execute(
        """
        INSERT INTO interactions (user_id, item_id, event, timestamp)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (user_id, item_id, event)
    )
    conn.commit()


def get_interactions_df() -> pd.DataFrame:
    """Возвращает все взаимодействия как pandas DataFrame."""
    return pd.read_sql_query("SELECT * FROM interactions", conn)
