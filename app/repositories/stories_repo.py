from app.db import get_db


def recent_stories(limit=8):
    return get_db().execute(
        """SELECT stories.*, users.username, users.pronouns, cities.slug as city_slug, cities.name as city_name
           FROM stories
           JOIN users ON stories.user_id = users.id
           LEFT JOIN cities ON stories.city_id = cities.id
           ORDER BY stories.created_at DESC LIMIT ?""",
        (limit,),
    ).fetchall()


def stories_for_city(city_id, limit=6):
    return get_db().execute(
        """SELECT stories.*, users.username, users.pronouns
           FROM stories JOIN users ON stories.user_id = users.id
           WHERE stories.city_id = ?
           ORDER BY stories.created_at DESC LIMIT ?""",
        (city_id, limit),
    ).fetchall()
