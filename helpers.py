"""Helper functions for QueerNomads."""

from functools import wraps
from flask import redirect, session, render_template


def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    """Render an apology/error message to the user."""
    return render_template("apology.html", message=message, code=code), code
