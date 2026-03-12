"""Read-only city routes for early city-intelligence foundation."""

from flask import Blueprint, render_template, request

from app.services.city_service import (
    ALLOWED_SORT_FIELDS,
    CityDiscoveryParams,
    get_all_cities,
    get_city_by_slug,
    get_city_data_notice,
    get_methodology_content,
    get_regions,
    get_related_cities,
    get_score_breakdown,
)
from helpers import apology


city_bp = Blueprint("city", __name__)


def _parse_float_arg(name: str) -> float | None:
    """Parse numeric threshold query params safely."""
    raw_value = request.args.get(name, "").strip()
    if raw_value == "":
        return None
    try:
        value = float(raw_value)
    except ValueError:
        return None

    if value < 0:
        return 0.0
    if value > 10:
        return 10.0
    return value


@city_bp.route("/cities")
def list_cities():
    """List seeded city intelligence entries with discovery controls."""
    region = request.args.get("region", "").strip()
    available_regions = get_regions()
    if region and region not in available_regions:
        region = ""

    sort = request.args.get("sort", "overall_score").strip()
    if sort not in ALLOWED_SORT_FIELDS:
        sort = "overall_score"

    discovery_params = CityDiscoveryParams(
        q=request.args.get("q", "").strip(),
        region=region,
        sort=sort,
        min_affordability=_parse_float_arg("min_affordability"),
        min_safety=_parse_float_arg("min_safety"),
        min_internet=_parse_float_arg("min_internet"),
        min_weather=_parse_float_arg("min_weather"),
        min_inclusivity=_parse_float_arg("min_inclusivity"),
    )

    cities = get_all_cities(discovery_params)

    return render_template(
        "cities.html",
        cities=cities,
        data_notice=get_city_data_notice(),
        query=discovery_params,
        available_regions=available_regions,
        available_sort_fields=list(ALLOWED_SORT_FIELDS.keys()),
    )


@city_bp.route("/cities/<slug>")
def view_city(slug: str):
    """View one city intelligence profile by slug."""
    city = get_city_by_slug(slug)
    if city is None:
        return apology("City not found", 404)

    return render_template(
        "city_detail.html",
        city=city,
        data_notice=get_city_data_notice(),
        score_breakdown=get_score_breakdown(city),
        related_cities=get_related_cities(slug),
    )


@city_bp.route("/methodology")
def methodology():
    """Explain city intelligence methodology and confidence labeling."""
    return render_template(
        "methodology.html",
        methodology=get_methodology_content(),
        data_notice=get_city_data_notice(),
    )


@city_bp.app_context_processor
def inject_seed_city_count():
    """Expose seed city count for shared templates and nav context."""
    return {"seed_city_count": len(get_all_cities())}
