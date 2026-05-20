"""Тесты рекомендательной системы."""

import pandas as pd

from src.recommender import (
    popularity_scores,
    content_scores,
    get_recommendations
)


def test_popularity_scores():
    """Проверка функции популярности."""
    scores = popularity_scores()
    assert isinstance(scores, dict)
    assert len(scores) > 0


def test_content_scores():
    """Проверка content-based рекомендаций."""
    scores = content_scores(1)  # user_id = 1
    assert isinstance(scores, dict)


def test_get_recommendations():
    """Проверка основной функции рекомендаций."""
    recommendations = get_recommendations(1)

    assert isinstance(recommendations, pd.DataFrame)

    # Проверяем структуру возвращаемого DataFrame
    expected = ["item_id", "title", "domain", "description"]
    assert list(recommendations.columns) == expected
