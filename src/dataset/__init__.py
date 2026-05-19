"""Данные о всех объектах (фильмы, книги, курсы)."""

import pandas as pd

items = [
    [1, "Interstellar", "movie", "space sci-fi future"],
    [2, "The Matrix", "movie", "ai sci-fi cyberpunk"],
    [3, "Harry Potter", "book", "magic fantasy wizard"],
    [4, "Lord of the Rings", "book", "fantasy adventure"],
    [5, "Python Course", "course", "programming python beginner"],
    [6, "ML Course", "course", "machine learning ai data"],
    [7, "Inception", "movie", "dream thriller sci-fi"],
    [8, "Data Science Book", "book", "data science analysis"],
    [9, "Web Dev Course", "course", "javascript html css"],
]

items_df = pd.DataFrame(items, columns=["item_id", "title", "domain", "description"])
