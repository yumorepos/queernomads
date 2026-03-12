from flask import Blueprint, render_template, request
from app.repositories.cities_repo import get_city_by_slug, list_cities_with_scores, list_regions
from app.repositories.stories_repo import stories_for_city
from app.services.city_filters import SORT_OPTIONS, apply_city_filters
from app.services.ranking_presets import PRESET_DEFINITIONS, valid_preset

bp = Blueprint("cities", __name__, url_prefix="/cities")


@bp.route("")
def city_index():
    region = request.args.get("region", "")
    cost_level = request.args.get("cost_level", "")
    min_score = request.args.get("min_score", "")
    sort = request.args.get("sort", "score_desc")
    preset = valid_preset(request.args.get("preset", "balanced"))

    cities = list_cities_with_scores(preset=preset)
    filtered = apply_city_filters(
        cities,
        region=region or None,
        cost_level=cost_level or None,
        min_score=min_score or None,
        sort=sort,
    )

    return render_template(
        "cities/index.html",
        cities=filtered,
        regions=list_regions(),
        selected_region=region,
        selected_cost=cost_level,
        min_score=min_score,
        sort=sort if sort in SORT_OPTIONS else "score_desc",
        preset=preset,
        presets=PRESET_DEFINITIONS,
    )


@bp.route("/<slug>")
def city_detail(slug):
    city = get_city_by_slug(slug)
    if not city:
        return render_template("apology.html", message="City not found", code=404), 404

    insights = stories_for_city(city["id"])
    return render_template("cities/detail.html", city=city, insights=insights)
