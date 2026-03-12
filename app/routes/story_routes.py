"""Story routes: posting, browsing, and reading stories."""

from flask import Blueprint, flash, redirect, render_template, request, session

from helpers import login_required, apology
from app.models.story import VALID_STORY_CATEGORIES
from app.services.story_service import browse_stories, create_story, get_story_by_id


story_bp = Blueprint("story", __name__)


@story_bp.route("/post", methods=["GET", "POST"])
@login_required
def post_story():
    """Create a new travel story."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        destination = request.form.get("destination", "").strip()
        category = request.form.get("category", "")
        rating = request.form.get("rating", "")
        body = request.form.get("body", "").strip()

        if not title:
            return apology("Please provide a title")
        if not destination:
            return apology("Please provide a destination")
        if category not in VALID_STORY_CATEGORIES:
            return apology("Please select a valid category")

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            return apology("Please provide a rating between 1 and 5")

        if not body:
            return apology("Please write your story")

        create_story(session["user_id"], title, destination, category, rating, body)
        flash("Your story has been shared! ✨", "success")
        return redirect("/")

    return render_template("post.html")


@story_bp.route("/browse")
def browse():
    """Browse and search stories."""
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "")

    if category and category not in VALID_STORY_CATEGORIES:
        category = ""

    stories, destinations = browse_stories(query=query, category=category)

    return render_template(
        "browse.html",
        stories=stories,
        query=query,
        selected_category=category,
        destinations=destinations,
    )


@story_bp.route("/story/<int:story_id>")
def view_story(story_id):
    """View a single story."""
    story = get_story_by_id(story_id)

    if not story:
        return apology("Story not found", 404)

    return render_template("story.html", story=story)
