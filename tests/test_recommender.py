"""Тесты рекомендательной системы."""

import os
import sys

import pandas as pd

# Добавляем корень проекта в PYTHONPATH
root_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, root_dir)

from src.recommender import (
    content_scores,
    get_recommendations,
    popularity_scores,
)


def test_popularity_scores():
    """Проверка функции популярности."""
    scores = popularity_scores()

    assert isinstance(scores, dict)
    assert len(scores) > 0


def test_content_scores():
    """Проверка content-based рекомендаций."""
    scores = content_scores(1)

    assert isinstance(scores, dict)


def test_get_recommendations():
    """Проверка основной функции рекомендаций."""
    recommendations = get_recommendations(1)

    assert isinstance(recommendations, pd.DataFrame)

    expected_columns = [
        "item_id",
        "title",
        "domain",
        "description",
    ]

    assert list(recommendations.columns) == expected_columns
    
