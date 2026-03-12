"""Story business logic and data access."""

from .db_service import get_db


def fetch_recent_stories(limit: int = 12):
    """Return recent stories with author fields for homepage feed."""
    db = get_db()
    return db.execute(
        """SELECT stories.*, users.username, users.pronouns
           FROM stories JOIN users ON stories.user_id = users.id
           ORDER BY stories.created_at DESC LIMIT ?""",
        (limit,),
    ).fetchall()


def create_story(user_id: int, title: str, destination: str, category: str, rating: int, body: str) -> None:
    """Insert a new story."""
    db = get_db()
    db.execute(
        "INSERT INTO stories (user_id, title, destination, category, rating, body) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, title, destination, category, rating, body),
    )
    db.commit()


def browse_stories(query: str = "", category: str = ""):
    """Search stories by optional query and category filters."""
    db = get_db()

    sql = """SELECT stories.*, users.username, users.pronouns
             FROM stories JOIN users ON stories.user_id = users.id"""
    params: list[str] = []
    conditions: list[str] = []

    if query:
        conditions.append("(stories.destination LIKE ? OR stories.title LIKE ?)")
        params.extend([f"%{query}%", f"%{query}%"])

    if category:
        conditions.append("stories.category = ?")
        params.append(category)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY stories.created_at DESC"

    stories = db.execute(sql, params).fetchall()
    destinations = db.execute("SELECT DISTINCT destination FROM stories ORDER BY destination").fetchall()

    return stories, destinations


def get_story_by_id(story_id: int):
    """Fetch one story with author metadata."""
    db = get_db()
    return db.execute(
        """SELECT stories.*, users.username, users.pronouns, users.home_city
           FROM stories JOIN users ON stories.user_id = users.id
           WHERE stories.id = ?""",
        (story_id,),
    ).fetchone()


def get_user_stories(user_id: int):
    """Fetch stories authored by a specific user."""
    db = get_db()
    return db.execute(
        "SELECT * FROM stories WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
