"""Данные о всех объектах (фильмы, книги, курсы) и пути к постерам."""

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

posters = {
    1: "images/1.jpg",   # Interstellar
    2: "images/2.jpg",   # The Matrix
    3: "images/3.jpg",   # Harry Potter
    4: "images/4.jpg",   # Lord of the Rings
    5: "images/5.jpg",   # Python Course
    6: "images/6.jpg",   # ML Course
    7: "images/7.jpg",   # Inception
    8: "images/8.jpg",   # Data Science Book
    9: "images/9.jpg",   # Web Dev Course
}
