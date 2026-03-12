"""Read-only city data access for city-intelligence routes."""

from datetime import date

from app.models.city import City, CityScoreMetadata


SEED_SCORE_METADATA = CityScoreMetadata(
    source_name="QueerNomads seed dataset",
    source_url="https://github.com/yumorepos/queernomads",
    methodology_note=(
        "These values are demo heuristics to prototype city intelligence. "
        "They are not authoritative real-world rankings."
    ),
    confidence_label="low",
    last_reviewed=date(2026, 3, 1),
    is_demo_data=True,
)


CITY_SEED_DATA = [
    City(
        slug="lisbon-portugal",
        name="Lisbon",
        country="Portugal",
        region="Europe",
        image="https://images.unsplash.com/photo-1585208798174-6cedd86e019a",
        summary="Popular base with strong coworking options and a visible queer-friendly social scene.",
        affordability=7.4,
        safety=8.0,
        internet=8.5,
        weather=9.0,
        inclusivity=8.1,
        overall_score=8.2,
        best_for=["remote workers", "mild weather", "community meetups"],
        score_metadata=SEED_SCORE_METADATA,
    ),
    City(
        slug="mexico-city-mexico",
        name="Mexico City",
        country="Mexico",
        region="North America",
        image="https://images.unsplash.com/photo-1512813195386-6cf811ad3542",
        summary="Large, dynamic city with rich queer culture and strong value for longer stays.",
        affordability=8.4,
        safety=6.7,
        internet=8.0,
        weather=7.8,
        inclusivity=7.6,
        overall_score=7.7,
        best_for=["food", "culture", "affordability"],
        score_metadata=SEED_SCORE_METADATA,
    ),
    City(
        slug="berlin-germany",
        name="Berlin",
        country="Germany",
        region="Europe",
        image="https://images.unsplash.com/photo-1560969184-10fe8719e047",
        summary="Historically important queer destination with strong inclusivity and dependable infrastructure.",
        affordability=6.4,
        safety=8.2,
        internet=8.8,
        weather=5.9,
        inclusivity=9.0,
        overall_score=7.7,
        best_for=["nightlife", "queer culture", "creative work"],
        score_metadata=SEED_SCORE_METADATA,
    ),
]


def get_all_cities(sort_by: str = "overall_score", descending: bool = True) -> list[City]:
    """Return all cities sorted by one supported field."""
    allowed_sort_keys = {
        "overall_score": lambda city: city.overall_score,
        "name": lambda city: city.name.lower(),
        "affordability": lambda city: city.affordability,
        "safety": lambda city: city.safety,
        "internet": lambda city: city.internet,
        "weather": lambda city: city.weather,
        "inclusivity": lambda city: city.inclusivity,
    }

    key_fn = allowed_sort_keys.get(sort_by, allowed_sort_keys["overall_score"])
    reverse = descending if sort_by != "name" else False
    return sorted(CITY_SEED_DATA, key=key_fn, reverse=reverse)


def get_city_by_slug(slug: str) -> City | None:
    """Get a single city by URL slug."""
    for city in CITY_SEED_DATA:
        if city.slug == slug:
            return city
    return None


def get_city_data_notice() -> str:
    """Shared transparency notice for city intelligence pages."""
    return (
        "City intelligence is currently based on demo seed data and heuristic scoring. "
        "Use it as directional guidance, not definitive truth."
    )
