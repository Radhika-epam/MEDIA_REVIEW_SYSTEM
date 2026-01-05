from database import get_connection


class ReviewNotifier:
    @staticmethod
    def notify_favorite_users(media_id, message):
        """
        Notify only users who have marked this media as favorite
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT users.name
            FROM favorites
            JOIN users ON users.user_id = favorites.user_id
            WHERE favorites.media_id = ?
        """, (media_id,))

        users = cursor.fetchall()
        conn.close()

        for (name,) in users:
            print(f"Notification for {name}: {message}")
