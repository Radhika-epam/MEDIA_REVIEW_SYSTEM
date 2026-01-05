from database import get_connection

# Function to submit a review
def submit_review(user_id, media_id, rating, comment):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reviews (user_id, media_id, rating, comment)
        VALUES (?, ?, ?, ?)
    """, (user_id, media_id, rating, comment))

    conn.commit()
    conn.close()


# ---------------- Notify users who favorited a media ----------------
def notify_favorites(media_id, reviewer_name):
    conn = get_connection()
    cursor = conn.cursor()

    # Get all users who have favorited this media
    cursor.execute("""
        SELECT u.name 
        FROM favorites f
        JOIN users u ON u.user_id = f.user_id
        WHERE f.media_id = ?
    """, (media_id,))

    users = cursor.fetchall()
    conn.close()

    if users:
        for (user_name,) in users:
            if user_name != reviewer_name:  # Optional: do not notify the reviewer themselves
                print(f"Notification: Hi {user_name}, media you favorited was just reviewed by {reviewer_name}!")
