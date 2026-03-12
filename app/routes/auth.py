from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
from helpers import apology

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not username or not email or not password:
            return apology("Please complete all required fields")
        if len(password) < 6 or password != confirmation:
            return apology("Password is invalid or does not match confirmation")

        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email)).fetchone()
        if existing:
            return apology("Username or email already taken")

        db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", (username, email, generate_password_hash(password)))
        db.commit()
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()["id"]
        flash("Welcome to QueerNomads! 🌈", "success")
        return redirect("/")

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not user or not check_password_hash(user["hash"], password):
            return apology("Invalid username or password", 403)
        session["user_id"] = user["id"]
        flash(f"Welcome back, {user['username']}! 🌈", "success")
        return redirect("/")
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You've been logged out.", "info")
    return redirect("/")
