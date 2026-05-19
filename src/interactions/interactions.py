from db_funcs import add_interaction_db

def add_interaction(user_id, item_id, event):
    add_interaction_db(user_id, item_id, event)
