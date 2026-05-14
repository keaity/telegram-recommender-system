import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from dataset import items_df
from database import get_interactions_df

weights = {"view":1, "like":3, "fav":5}

def popularity_scores():
    interactions = get_interactions_df()
    if interactions.empty:
        return {i:1 for i in items_df.item_id}

    df = interactions.copy()
    df["weight"] = df["event"].map(weights)
    pop = df.groupby("item_id")["weight"].sum()
    return pop.to_dict()

def collaborative_scores(user_id):
    interactions = get_interactions_df()
    if interactions.empty:
        return {}

    df = interactions.copy()
    df["weight"] = df["event"].map(weights)

    matrix = df.pivot_table(index="user_id", columns="item_id",
                            values="weight", fill_value=0)

    if user_id not in matrix.index or len(matrix.index) == 1:
        return {}   # нет других пользователей

    sim = cosine_similarity(matrix)
    sim_df = pd.DataFrame(sim, index=matrix.index, columns=matrix.index)
    similar_users = sim_df[user_id].sort_values(ascending=False)[1:]

    scores = {}
    for other_user, similarity in similar_users.items():
        user_items = matrix.loc[other_user]
        for item, value in user_items.items():
            scores[item] = scores.get(item,0) + similarity * value

    return scores

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(items_df["description"])
content_sim = cosine_similarity(tfidf_matrix)

def content_scores(user_id):
    interactions = get_interactions_df()
    user_items = interactions[interactions.user_id == user_id]["item_id"].unique()
    if len(user_items) == 0:
        return {}

    scores = {}
    for item in user_items:
        idx = item - 1
        sims = list(enumerate(content_sim[idx]))
        for i, score in sims:
            scores[i+1] = scores.get(i+1,0) + score

    return scores

def get_recommendations(user_id, top_n=5):
    interactions = get_interactions_df()
    user_history = interactions[interactions.user_id == user_id]["item_id"].unique()

    cf = collaborative_scores(user_id)
    cb = content_scores(user_id)
    pop = popularity_scores()

    final_scores = {}

    for item in items_df.item_id:
        final_scores[item] = (
            0.6 * cf.get(item,0) +
            0.3 * cb.get(item,0) +
            0.1 * pop.get(item,0)
        )

    for item in user_history:
        final_scores.pop(item, None)

    ranked = sorted(final_scores.items(),
                    key=lambda x: x[1], reverse=True)

    rec_ids = [i[0] for i in ranked[:top_n]]

    return items_df[items_df.item_id.isin(rec_ids)]
