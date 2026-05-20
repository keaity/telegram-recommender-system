"""Модуль рекомендательной системы (гибридный подход)."""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from dataset import items_df
from db_funcs import get_interactions_df

WEIGHTS = {"view": 1.0, "like": 3.0, "fav": 5.0}


def popularity_scores() -> dict:
    """Расчёт популярности объектов."""
    interactions = get_interactions_df()
    if interactions.empty:
        return {int(i): 1.0 for i in items_df.item_id}

    df = interactions.copy()
    df["weight"] = df["event"].map(WEIGHTS)
    pop = df.groupby("item_id")["weight"].sum()
    return pop.to_dict()


def content_scores(user_id: int) -> dict:
    """Content-based рекомендации по описаниям."""
    interactions = get_interactions_df()
    user_items = interactions[interactions.user_id == user_id]["item_id"].unique()

    if len(user_items) == 0:
        return {}

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(items_df["description"])
    content_sim = cosine_similarity(tfidf_matrix)

    scores = {}
    for item in user_items:
        idx = item - 1
        sims = list(enumerate(content_sim[idx]))
        for i, score in sims:
            scores[i + 1] = scores.get(i + 1, 0.0) + score
    return scores


def get_recommendations(user_id: int, top_n: int = 5) -> pd.DataFrame:
    """Основная функция получения рекомендаций."""
    interactions = get_interactions_df()
    user_history = interactions[interactions.user_id == user_id]["item_id"].unique()

    pop = popularity_scores()
    cb = content_scores(user_id)

    final_scores = {}
    for item_id in items_df.item_id:
        final_scores[item_id] = 0.4 * cb.get(item_id, 0.0) + 0.6 * pop.get(item_id, 1.0)

    for item in user_history:
        final_scores.pop(item, None)

    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    rec_ids = [i[0] for i in ranked[:top_n]]

    return items_df[items_df.item_id.isin(rec_ids)]
