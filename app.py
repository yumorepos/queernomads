"""
QueerNomads — A community platform for queer digital nomads to share travel experiences.
Built with Flask, SQLite, and Bootstrap 5.
"""

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

# Configure application
app = Flask(__name__)
app.secret_key = "queernomads-dev-secret-key-change-in-production"

# Database path
DATABASE = "queernomads.db"


def get_db():
    """Get database connection for current request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close database connection at end of request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database from schema.sql."""
    db = sqlite3.connect(DATABASE)
    with open("schema.sql") as f:
        db.executescript(f.read())
    db.close()


@app.context_processor
def inject_user():
    """Make current user available to all templates."""
    if session.get("user_id"):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        return {"current_user": user}
    return {"current_user": None}


# ─── Routes ──────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    """Homepage — show recent stories from the community."""
    db = get_db()
    stories = db.execute(
        """SELECT stories.*, users.username, users.pronouns
           FROM stories JOIN users ON stories.user_id = users.id
           ORDER BY stories.created_at DESC LIMIT 12"""
    ).fetchall()
    return render_template("index.html", stories=stories)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        # Validate inputs
        if not username:
            return apology("Please provide a username")
        if not email:
            return apology("Please provide an email")
        if not password:
            return apology("Please provide a password")
        if len(password) < 6:
            return apology("Password must be at least 6 characters")
        if password != confirmation:
            return apology("Passwords don't match")

        db = get_db()

        # Check if username/email already exists
        existing = db.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?", (username, email)
        ).fetchone()
        if existing:
            return apology("Username or email already taken")

        # Insert new user
        db.execute(
            "INSERT INTO users (username, email, hash) VALUES (?, ?, ?)",
            (username, email, generate_password_hash(password)),
        )
        db.commit()

        # Log them in
        user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        session["user_id"] = user["id"]
        flash("Welcome to QueerNomads! 🌈", "success")
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return apology("Please provide username and password")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if not user or not check_password_hash(user["hash"], password):
            return apology("Invalid username or password", 403)

        session["user_id"] = user["id"]
        flash(f"Welcome back, {user['username']}! 🌈", "success")
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""
    session.clear()
    flash("You've been logged out.", "info")
    return redirect("/")


@app.route("/post", methods=["GET", "POST"])
@login_required
def post_story():
    """Create a new travel story."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        destination = request.form.get("destination", "").strip()
        category = request.form.get("category", "")
        rating = request.form.get("rating", "")
        body = request.form.get("body", "").strip()

        # Validate
        if not title:
            return apology("Please provide a title")
        if not destination:
            return apology("Please provide a destination")
        if category not in ("nightlife", "safety", "community", "accommodation", "general"):
            return apology("Please select a valid category")
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            return apology("Please provide a rating between 1 and 5")
        if not body:
            return apology("Please write your story")

        db = get_db()
        db.execute(
            "INSERT INTO stories (user_id, title, destination, category, rating, body) VALUES (?, ?, ?, ?, ?, ?)",
            (session["user_id"], title, destination, category, rating, body),
        )
        db.commit()

        flash("Your story has been shared! ✨", "success")
        return redirect("/")

    return render_template("post.html")


@app.route("/browse")
def browse():
    """Browse and search stories."""
    db = get_db()
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "")

    sql = """SELECT stories.*, users.username, users.pronouns
             FROM stories JOIN users ON stories.user_id = users.id"""
    params = []
    conditions = []

    if query:
        conditions.append("(stories.destination LIKE ? OR stories.title LIKE ?)")
        params.extend([f"%{query}%", f"%{query}%"])

    if category and category in ("nightlife", "safety", "community", "accommodation", "general"):
        conditions.append("stories.category = ?")
        params.append(category)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY stories.created_at DESC"

    stories = db.execute(sql, params).fetchall()

    # Get all unique destinations for filter suggestions
    destinations = db.execute(
        "SELECT DISTINCT destination FROM stories ORDER BY destination"
    ).fetchall()

    return render_template(
        "browse.html",
        stories=stories,
        query=query,
        selected_category=category,
        destinations=destinations,
    )


@app.route("/story/<int:story_id>")
def view_story(story_id):
    """View a single story."""
    db = get_db()
    story = db.execute(
        """SELECT stories.*, users.username, users.pronouns, users.home_city
           FROM stories JOIN users ON stories.user_id = users.id
           WHERE stories.id = ?""",
        (story_id,),
    ).fetchone()

    if not story:
        return apology("Story not found", 404)

    return render_template("story.html", story=story)


@app.route("/profile/<int:user_id>")
def view_profile(user_id):
    """View a user's profile."""
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if not user:
        return apology("User not found", 404)

    stories = db.execute(
        "SELECT * FROM stories WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
    ).fetchall()

    return render_template("profile.html", user=user, stories=stories)


@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    """Edit your profile."""
    db = get_db()

    if request.method == "POST":
        bio = request.form.get("bio", "").strip()
        pronouns = request.form.get("pronouns", "").strip()
        home_city = request.form.get("home_city", "").strip()
        countries = request.form.get("countries_visited", "").strip()

        db.execute(
            """UPDATE users SET bio = ?, pronouns = ?, home_city = ?, countries_visited = ?
               WHERE id = ?""",
            (bio, pronouns, home_city, countries, session["user_id"]),
        )
        db.commit()

        flash("Profile updated! ✨", "success")
        return redirect(f"/profile/{session['user_id']}")

    user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return render_template("edit_profile.html", user=user)


# ─── Initialize ──────────────────────────────────────────────────────────────

# Create tables on first run
init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
