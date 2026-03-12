from flask import Blueprint, render_template, request
from app.repositories.cities_repo import get_city_by_slug, list_cities_with_scores
from app.services.comparison import build_comparison_matrix

bp = Blueprint("compare", __name__)


@bp.route("/compare")
def compare():
    requested = request.args.getlist("city")[:4]
    selected = [get_city_by_slug(slug) for slug in requested if slug]
    selected = [city for city in selected if city]
    matrix = build_comparison_matrix(selected)
    all_cities = sorted(list_cities_with_scores(), key=lambda c: c["name"])
    return render_template("compare.html", selected=selected, matrix=matrix, all_cities=all_cities)
