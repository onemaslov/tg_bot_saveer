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
                    user_id INTEGER UNIQUE,
                    username TEXT
                )
                """
            )


def add_user(user_id: int, username: str | None) -> None:
    """Insert user into database, ignoring duplicates."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT OR IGNORE INTO users(user_id, username) VALUES(?, ?)",
                (user_id, username),
            )


def get_all_users() -> list[tuple[int, str | None]]:
    """Return list of tuples (user_id, username)."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT user_id, username FROM users ORDER BY id")
        return cur.fetchall()
