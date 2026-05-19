"""Логика добавления взаимодействий пользователя."""

from db_funcs import add_interaction_db


def add_interaction(user_id: int, item_id: int, event: str) -> None:
    """Добавляет взаимодействие (view/like/fav)."""
    add_interaction_db(user_id, item_id, event)

