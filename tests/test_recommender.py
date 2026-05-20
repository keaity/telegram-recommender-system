"""Тесты рекомендательной системы."""

import pandas as pd

from src.recommender.recommender import (
    popularity_scores,
    content_scores,
    get_recommendations,
)


def test_popularity_scores():
    """Проверка popular recommendations."""
    scores = popularity_scores()

    assert isinstance(scores, dict)


def test_content_scores():
    """Проверка content-based части."""
    scores = content_scores(1)

    assert isinstance(scores, dict)


def test_get_recommendations():
    """Проверка получения рекомендаций."""
    recommendations = get_recommendations(1)

    assert isinstance(recommendations, pd.DataFrame)
