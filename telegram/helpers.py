import os
import json

HISTORY_DIR = "storage/history/"
HISTORY_LIMIT = 20 * 2  # each message takes 2 turns


def ensure_history_dir_exists():
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)


def get_history(user_id):
    try:
        with open(HISTORY_DIR + f"{user_id}.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    
    return history


def add_to_history(user_id, message):
    """Format of message: {"role": "user/model", "content": str}"""
    history = get_history(user_id)
    
    history.append(message)
    
    if len(history) > HISTORY_LIMIT:
        history = history[-HISTORY_LIMIT:]
    
    path = HISTORY_DIR + f"{user_id}.json"
    with open(path, "w") as f:
        json.dump(history, f)


def clear_history(user_id):
    path = HISTORY_DIR + f"{user_id}.json"
    with open(path, "w") as f:
        f.write("[]")
