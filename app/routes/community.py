from flask import Blueprint, flash, redirect, render_template, request, session

from app.db import get_db
from helpers import apology, login_required

bp = Blueprint("community", __name__)


@bp.route("/community")
@bp.route("/browse")
def browse():
    db = get_db()
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "")

    sql = """SELECT stories.*, users.username, users.pronouns, cities.slug as city_slug
             FROM stories JOIN users ON stories.user_id = users.id
             LEFT JOIN cities ON stories.city_id = cities.id"""
    params, conditions = [], []

    if query:
        conditions.append("(stories.destination LIKE ? OR stories.title LIKE ?)")
        params.extend([f"%{query}%", f"%{query}%"])

    if category and category in ("nightlife", "safety", "community", "accommodation", "general"):
        conditions.append("stories.category = ?")
        params.append(category)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    stories = db.execute(sql + " ORDER BY stories.created_at DESC", params).fetchall()
    return render_template("community/index.html", stories=stories, query=query, selected_category=category)


@bp.route("/post", methods=["GET", "POST"])
@login_required
def post_story():
    db = get_db()
    cities = db.execute("SELECT id, name FROM cities ORDER BY name").fetchall()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        destination = request.form.get("destination", "").strip()
        category = request.form.get("category", "")
        rating = request.form.get("rating", "")
        body = request.form.get("body", "").strip()
        city_id = request.form.get("city_id") or None

        if not title or not destination or not body:
            return apology("Please complete title, destination, and story")
        if category not in ("nightlife", "safety", "community", "accommodation", "general"):
            return apology("Please select a valid category")
        try:
            rating = int(rating)
            assert 1 <= rating <= 5
        except Exception:
            return apology("Please provide a rating between 1 and 5")

        db.execute(
            """INSERT INTO stories (user_id, city_id, title, destination, category, rating, body)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (session["user_id"], city_id, title, destination, category, rating, body),
        )
        db.commit()
        flash("Your story has been shared! ✨", "success")
        return redirect("/community")

    return render_template("post.html", cities=cities)


@bp.route("/story/<int:story_id>")
def view_story(story_id):
    db = get_db()
    story = db.execute(
        """SELECT stories.*, users.username, users.pronouns, users.home_city, cities.slug AS city_slug, cities.name AS city_name
           FROM stories JOIN users ON stories.user_id = users.id
           LEFT JOIN cities ON stories.city_id = cities.id
           WHERE stories.id = ?""",
        (story_id,),
    ).fetchone()
    if not story:
        return apology("Story not found", 404)
    return render_template("story.html", story=story)


@bp.route("/profile/<int:user_id>")
def view_profile(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return apology("User not found", 404)
    stories = db.execute("SELECT * FROM stories WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    return render_template("profile.html", user=user, stories=stories)


@bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    db = get_db()
    if request.method == "POST":
        db.execute(
            "UPDATE users SET bio = ?, pronouns = ?, home_city = ?, countries_visited = ? WHERE id = ?",
            (
                request.form.get("bio", "").strip(),
                request.form.get("pronouns", "").strip(),
                request.form.get("home_city", "").strip(),
                request.form.get("countries_visited", "").strip(),
                session["user_id"],
            ),
        )
        db.commit()
        flash("Profile updated! ✨", "success")
        return redirect(f"/profile/{session['user_id']}")

    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return render_template("edit_profile.html", user=user)
