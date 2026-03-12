"""City routes placeholder for upcoming city-intelligence features."""

from flask import Blueprint

from app.services.city_service import get_seed_cities


city_bp = Blueprint("city", __name__)


@city_bp.app_context_processor
def inject_seed_city_count():
    """Expose seed city count for future templates without changing current UX."""
    return {"seed_city_count": len(get_seed_cities())}
