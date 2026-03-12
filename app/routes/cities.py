from flask import Blueprint, render_template, request
from app.repositories.cities_repo import get_city_by_slug, list_cities_with_scores, list_regions
from app.repositories.stories_repo import stories_for_city
from app.services.city_filters import apply_city_filters

bp = Blueprint("cities", __name__, url_prefix="/cities")


@bp.route("")
def city_index():
    region = request.args.get("region", "")
    cost_level = request.args.get("cost_level", "")
    min_score = request.args.get("min_score", "")
    sort = request.args.get("sort", "overall_desc")

    cities = list_cities_with_scores()
    filtered = apply_city_filters(cities, region=region or None, cost_level=cost_level or None, min_score=min_score or None, sort=sort)

    return render_template(
        "cities/index.html",
        cities=filtered,
        regions=list_regions(),
        selected_region=region,
        selected_cost=cost_level,
        min_score=min_score,
        sort=sort,
    )


@bp.route("/<slug>")
def city_detail(slug):
    city = get_city_by_slug(slug)
    if not city:
        return render_template("apology.html", message="City not found", code=404), 404

    insights = stories_for_city(city["id"])
    return render_template("cities/detail.html", city=city, insights=insights)
