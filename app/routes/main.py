from flask import Blueprint, render_template
from app.repositories.cities_repo import list_cities_with_scores
from app.repositories.stories_repo import recent_stories

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    cities = sorted(list_cities_with_scores(), key=lambda c: c["overall_score"], reverse=True)[:3]
    stories = recent_stories(limit=6)
    return render_template("index.html", featured_cities=cities, stories=stories)
