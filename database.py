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
                    message_count INTEGER DEFAULT 0,
                    UNIQUE(chat_id, user_id)
                )
                """
            )

            # Миграция старых схем без поля chat_id
            cur = conn.execute("PRAGMA table_info(users)")
            columns = [row[1] for row in cur.fetchall()]
            if "chat_id" not in columns:
                conn.execute("ALTER TABLE users ADD COLUMN chat_id INTEGER")
            if "message_count" not in columns:
                conn.execute("ALTER TABLE users ADD COLUMN message_count INTEGER DEFAULT 0")

            # Уникальный индекс, если он отсутствует (для старых таблиц)
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_chat_user ON users(chat_id, user_id)"
            )


def add_user(chat_id: int, user_id: int, username: str | None) -> None:
    """Insert user for given chat, ignoring duplicates."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT OR IGNORE INTO users(chat_id, user_id, username, message_count) VALUES(?, ?, ?, 0)",
                (chat_id, user_id, username),
            )


def record_message(chat_id: int, user_id: int, username: str | None) -> None:
    """Insert user if needed and increment message_count."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            # insert
            conn.execute(
                "INSERT OR IGNORE INTO users(chat_id, user_id, username, message_count) VALUES(?, ?, ?, 0)",
                (chat_id, user_id, username),
            )
            # update count
            conn.execute(
                "UPDATE users SET message_count = message_count + 1, username = COALESCE(?, username) WHERE chat_id = ? AND user_id = ?",
                (username, chat_id, user_id),
            )


def get_users(chat_id: int) -> list[tuple[int, str | None, int]]:
    """Return list of tuples (user_id, username, message_count) for given chat."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, username, message_count FROM users WHERE chat_id = ? ORDER BY message_count DESC",
            (chat_id,),
        )
        return cur.fetchall()
