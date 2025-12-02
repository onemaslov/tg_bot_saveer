import sqlite3
from contextlib import closing

DB_PATH = "users.db"


def init_db() -> None:
    """Create the users table if it does not exist."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    user_id INTEGER,
                    username TEXT,
                    UNIQUE(chat_id, user_id)
                )
                """
            )


def add_user(chat_id: int, user_id: int, username: str | None) -> None:
    """Insert user for given chat, ignoring duplicates."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT OR IGNORE INTO users(chat_id, user_id, username) VALUES(?, ?, ?)",
                (chat_id, user_id, username),
            )


def get_users(chat_id: int) -> list[tuple[int, str | None]]:
    """Return list of tuples (user_id, username) for given chat."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, username FROM users WHERE chat_id = ? ORDER BY id",
            (chat_id,),
        )
        return cur.fetchall()
