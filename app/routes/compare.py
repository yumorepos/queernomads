from flask import Blueprint, render_template, request
from app.repositories.cities_repo import get_city_by_slug, list_cities_with_scores
from app.services.comparison import build_comparison_matrix, normalize_city_selection

bp = Blueprint("compare", __name__)


@bp.route("/compare")
def compare():
    requested = request.args.getlist("city")
    selected_slugs, duplicates = normalize_city_selection(requested)

    selected = []
    invalid = []
    for slug in selected_slugs:
        city = get_city_by_slug(slug)
        if city:
            selected.append(city)
        else:
            invalid.append(slug)

    matrix = build_comparison_matrix(selected)
    all_cities = sorted(list_cities_with_scores(), key=lambda c: c["name"])

    winner_counts = [0] * len(selected)
    for row in matrix:
        winner_index = row.get("winner_index")
        if winner_index is not None and winner_index < len(winner_counts):
            winner_counts[winner_index] += 1

    warning = None
    if invalid:
        warning = f"Some selected cities were unavailable and were skipped: {', '.join(invalid)}"
    elif duplicates:
        warning = "Duplicate cities were removed from your comparison selection."

    return render_template(
        "compare.html",
        selected=selected,
        matrix=matrix,
        all_cities=all_cities,
        warning=warning,
        winner_counts=winner_counts,
    )
