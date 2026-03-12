"""Main routes: homepage, auth, and profiles."""

from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology
from app.services.db_service import get_db
from app.services.story_service import fetch_recent_stories, get_user_stories


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Homepage — show recent stories from the community."""
    stories = fetch_recent_stories(limit=12)
    return render_template("index.html", stories=stories)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

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
        existing = db.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?", (username, email)
        ).fetchone()
        if existing:
            return apology("Username or email already taken")

        db.execute(
            "INSERT INTO users (username, email, hash) VALUES (?, ?, ?)",
            (username, email, generate_password_hash(password)),
        )
        db.commit()

        user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        session["user_id"] = user["id"]
        flash("Welcome to QueerNomads! 🌈", "success")
        return redirect("/")

    return render_template("register.html")


@main_bp.route("/login", methods=["GET", "POST"])
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


@main_bp.route("/logout")
def logout():
    """Log user out."""
    session.clear()
    flash("You've been logged out.", "info")
    return redirect("/")


@main_bp.route("/profile/<int:user_id>")
def view_profile(user_id):
    """View a user's profile."""
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if not user:
        return apology("User not found", 404)

    stories = get_user_stories(user_id)
    return render_template("profile.html", user=user, stories=stories)


@main_bp.route("/profile/edit", methods=["GET", "POST"])
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
