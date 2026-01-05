import argparse
from database import setup_database, get_connection
from services.review_services import submit_review, notify_favorites
from services.recommendation import get_recommendations

# ----------------- Setup -----------------
setup_database()

# ----------------- Helper -----------------
def display_top_rated(rows):
    print("\nTop Rated Media:\n")
    print("{:<10} {:<25} {:<10}".format("Media ID", "Title", "Avg Rating"))
    print("-" * 50)
    for media_id, title, avg_rating in rows:
        print("{:<10} {:<25} {:<10}".format(media_id, title, round(avg_rating, 2)))
    print()

def display_media(rows):
    print("\nMedia List:\n")
    print("{:<10} {:<25} {:<10}".format("Media ID", "Title", "Type"))
    print("-" * 50)
    for media_id, title, mtype in rows:
        print("{:<10} {:<25} {:<10}".format(media_id, title, mtype))
    print()

# ----------------- CLI Arguments -----------------
parser = argparse.ArgumentParser(description="Media Review System (CLI)")
parser.add_argument("--list", action="store_true")
parser.add_argument("--review", action="store_true")
parser.add_argument("--reviews", action="store_true")
parser.add_argument("--favorite", action="store_true")
parser.add_argument("--recommend", action="store_true")
parser.add_argument("--top-rated", action="store_true")
parser.add_argument("--search", action="store_true")  # Search option

args = parser.parse_args()

conn = get_connection()
cursor = conn.cursor()

# ----------------- Commands -----------------
if args.list:
    cursor.execute("SELECT * FROM media")
    rows = cursor.fetchall()
    if not rows:
        print("No media available")
    else:
        display_media(rows)

elif args.review:
    try:
        user_name = input("Enter Your Name: ").strip()

        cursor.execute("SELECT user_id FROM users WHERE name = ?", (user_name,))
        user = cursor.fetchone()

        if not user:
            cursor.execute("INSERT INTO users (name) VALUES (?)", (user_name,))
            conn.commit()
            user_id = cursor.lastrowid
        else:
            user_id = user[0]

        media_id = int(input("Enter Media ID: "))
        cursor.execute("SELECT media_id FROM media WHERE media_id = ?", (media_id,))
        if not cursor.fetchone():
            print("Invalid Media ID")
            conn.close()
            exit()

        rating = int(input("Enter Rating (1-5): "))
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5")
            conn.close()
            exit()

        comment = input("Enter Comment: ")
        submit_review(user_id, media_id, rating, comment)
        print("Review stored successfully in database")

        # ---------------- Notify users who favorited this media ----------------
        notify_favorites(media_id, user_name)

    except ValueError:
        print("Invalid input. Please enter numbers where required.")

elif args.reviews:
    cursor.execute("SELECT COUNT(*) FROM reviews")
    print(f"Total reviews stored: {cursor.fetchone()[0]}")

elif args.favorite:
    try:
        user_id = int(input("Enter User ID: "))
        media_id = int(input("Enter Media ID to favorite: "))

        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            print("User ID not found")
        else:
            cursor.execute(
                "INSERT OR IGNORE INTO favorites (user_id, media_id) VALUES (?, ?)",
                (user_id, media_id)
            )
            conn.commit()
            print("Media added to favorites")
    except ValueError:
        print("Invalid User ID or Media ID")

elif args.top_rated:
    cursor.execute("""
        SELECT m.media_id, m.title, AVG(r.rating) AS avg_rating
        FROM reviews r
        JOIN media m ON m.media_id = r.media_id
        GROUP BY m.media_id
        ORDER BY avg_rating DESC
    """)
    rows = cursor.fetchall()
    if not rows:
        print("No ratings available yet")
    else:
        display_top_rated(rows)

elif args.recommend:
    try:
        user_id = int(input("Enter User ID: "))
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            print("User ID not found")
        else:
            recommendations = get_recommendations(user_id)
            if not recommendations:
                print("No personalized recommendations available")
            else:
                print("\nRecommended Media:\n")
                print("{:<25} {:<10}".format("Title", "Avg Rating"))
                print("-" * 40)
                for title, avg_rating in recommendations:
                    print("{:<25} {:<10}".format(title, avg_rating))
                print()
    except ValueError:
        print("Invalid User ID input")

elif args.search:
    search_term = input("Enter media title to search: ").strip()
    cursor.execute(
        "SELECT media_id, title, type FROM media WHERE title LIKE ?",
        ('%' + search_term + '%',)
    )
    rows = cursor.fetchall()
    if not rows:
        print("No media found matching your search")
    else:
        display_media(rows)

else:
    print("""
Available Commands:
-------------------
python media_review.py --list
python media_review.py --review
python media_review.py --reviews
python media_review.py --favorite
python media_review.py --top-rated
python media_review.py --recommend
python media_review.py --search
""")

conn.close()
