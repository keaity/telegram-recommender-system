import sqlite3
import pandas as pd

conn = sqlite3.connect("recsys.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        user_id INTEGER,
        item_id INTEGER,
        event TEXT
    )
    """)
    conn.commit()


def add_interaction_db(user_id, item_id, event):
    cursor.execute(
        "INSERT INTO interactions VALUES (?, ?, ?)",
        (user_id, item_id, event)
    )
    conn.commit()


def get_interactions_df():
    return pd.read_sql_query("SELECT * FROM interactions", conn)
