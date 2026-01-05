import sqlite3

DB_NAME = "media_review.db"

# ----------------- Helper: Get DB connection -----------------
def get_connection():
    return sqlite3.connect(DB_NAME)


# ----------------- Fetch media already reviewed by the user -----------------
def get_reviewed_media(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT media_id FROM reviews WHERE user_id = ?", (user_id,))
    reviewed = {row[0] for row in cursor.fetchall()}
    conn.close()
    return reviewed


# ----------------- Get recommendations for a user -----------------
def get_recommendations(user_id):
    reviewed = get_reviewed_media(user_id)
    conn = get_connection()
    cursor = conn.cursor()

    if reviewed:
        # Recommend media not yet reviewed by the user, ordered by avg rating
        placeholders = ','.join('?' * len(reviewed))
        query = f"""
            SELECT m.title, AVG(r.rating) as avg_rating
            FROM media m
            LEFT JOIN reviews r ON m.media_id = r.media_id
            WHERE m.media_id NOT IN ({placeholders})
            GROUP BY m.media_id
            ORDER BY avg_rating DESC
        """
        cursor.execute(query, tuple(reviewed))
    else:
        # User has not reviewed anything yet: recommend top-rated media
        query = """
            SELECT m.title, AVG(r.rating) as avg_rating
            FROM media m
            LEFT JOIN reviews r ON m.media_id = r.media_id
            GROUP BY m.media_id
            ORDER BY avg_rating DESC
        """
        cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    # Replace None ratings with 0
    recommendations = [(title, avg_rating if avg_rating else 0) for title, avg_rating in rows]
    return recommendations
