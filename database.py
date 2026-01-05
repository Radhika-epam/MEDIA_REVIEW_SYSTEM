import sqlite3

DB_NAME = "media_review.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media (
        media_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        media_id INTEGER,
        rating INTEGER,
        comment TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(media_id) REFERENCES media(media_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        user_id INTEGER,
        media_id INTEGER,
        UNIQUE(user_id, media_id)
    )
    """)

    conn.commit()
    conn.close()
