Media Review System (Python CLI Project)

A **Media Review System** built using **Python**, **SQLite**, and **Object-Oriented Design Patterns**.
The application allows users to review media (movies, songs, series), mark favorites, receive notifications, and get personalized recommendations using **user-based collaborative filtering**.

---

## Features

### User Management

* Users are **created dynamically** while adding reviews
* No manual database insertion required
* Each user has a unique `user_id`

### Media Management

* Media stored with:

  * Media ID
  * Title
  * Type (Movie / Song / Series)

### Review System

* Add reviews using **Media ID**
* Rating (1–5) with comments
* Reviews stored persistently in SQLite
* Supports concurrent review submission using **multithreading**

### Favorites

* Users can mark media as favorite
* Favorite relationships stored in database

### Notifications (Observer Pattern)

* When a media is reviewed, users who favorited that media are notified
* Demonstrates real-world observer pattern usage

### Personalized Recommendations

* Implements **User-Based Collaborative Filtering**
* Recommends:

  * Media liked by similar users
  * Media **not yet reviewed by the current user**
* Uses average ratings from similar users

### Top Rated Media

* Displays top-rated media based on average ratings
* Sorted in descending order

### Search

* Search media by title keyword using CLI

### Caching

* Redis-based caching layer (optional performance optimization)

---

## Design Patterns Used

| Pattern                       | Purpose                                      |
| ----------------------------- | -------------------------------------------- |
| **Factory Pattern**           | Create different media types                 |
| **Observer Pattern**          | Notify users when favorite media is reviewed |
| **Singleton (DB connection)** | Manage database connections efficiently      |

---

## Project Structure

```
media-review-system/
│
├── media_review.py        # CLI application (entry point)
├── database.py            # SQLite database setup & connection
├── cache.py               # Redis caching logic
├── README.md
│
├── models/
│   ├── media.py           # Media base & subclasses
│   ├── user.py            # User model
│   └── review.py          # Review model
│
├── patterns/
│   ├── factory.py         # Factory Pattern
│   └── observer.py        # Observer Pattern
│
├── services/
│   ├── review_services.py # Review logic + multithreading
│   └── recommendation.py # Recommendation logic
│
└── media_review.db        # Auto-created SQLite DB (ignored in Git)
```

---

## Technologies Used

* **Python 3**
* **SQLite**
* **Redis**
* **Multithreading**
* **OOP & Design Patterns**
* **Git & GitHub**

---

## How to Run the Project

### Clone the repository

```bash
git clone https://github.com/Radhika-epam/MEDIA_REVIEW_SYSTEM.git
cd MEDIA_REVIEW_SYSTEM
```

### Run the CLI

```bash
python media_review.py
```

---

## Available Commands

```bash
python media_review.py --list        # List all media
python media_review.py --review      # Add a review
python media_review.py --reviews     # View all reviews
python media_review.py --favorite    # Add favorite media
python media_review.py --search      # Search media
python media_review.py --top-rated   # View top rated media
python media_review.py --recommend   # Get personalized recommendations
```

---

## Multithreading Support

* Review submissions are handled using **threads**
* Improves performance under concurrent operations
* Unit tests can be added using `unittest` or `pytest`

---

## Recommendation Logic (Brief)

* Find users with similar rating patterns
* Extract media they liked
* Filter out media already reviewed by current user
* Rank by average rating

---

## Database

* Automatically created (`media_review.db`)
* Tables:

  * users
  * media
  * reviews
  * favorites
* Database file is **ignored in Git** for best practices

---

