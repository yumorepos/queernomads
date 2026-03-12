"""Read-only city routes for early city-intelligence foundation."""

from flask import Blueprint, render_template

from app.services.city_service import get_all_cities, get_city_by_slug, get_city_data_notice
from helpers import apology


city_bp = Blueprint("city", __name__)


@city_bp.route("/cities")
def list_cities():
    """List seeded city intelligence entries."""
    cities = get_all_cities()
    return render_template(
        "cities.html",
        cities=cities,
        data_notice=get_city_data_notice(),
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
    )


@city_bp.app_context_processor
def inject_seed_city_count():
    """Expose seed city count for shared templates and nav context."""
    return {"seed_city_count": len(get_all_cities())}
