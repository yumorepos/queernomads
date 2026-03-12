"""Read-only city data access for city-intelligence routes."""

from dataclasses import dataclass
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
        tradeoff_summary=(
            "Lisbon balances strong internet, weather, and inclusivity signals with rising costs in popular "
            "neighborhoods and seasonal crowding."
        ),
        affordability=7.4,
        safety=8.0,
        internet=8.5,
        weather=9.0,
        inclusivity=8.1,
        overall_score=8.2,
        best_for=["remote workers", "mild weather", "community meetups"],
        strengths=["Reliable coworking ecosystem", "Strong year-round climate", "Visible queer social spaces"],
        limitations=["Housing competition in central areas", "Summer tourism pressure"],
        score_metadata=SEED_SCORE_METADATA,
    ),
    City(
        slug="mexico-city-mexico",
        name="Mexico City",
        country="Mexico",
        region="North America",
        image="https://images.unsplash.com/photo-1512813195386-6cf811ad3542",
        summary="Large, dynamic city with rich queer culture and strong value for longer stays.",
        tradeoff_summary=(
            "Mexico City offers affordability and culture depth, but requires neighborhood-level planning for "
            "safety and commute quality."
        ),
        affordability=8.4,
        safety=6.7,
        internet=8.0,
        weather=7.8,
        inclusivity=7.6,
        overall_score=7.7,
        best_for=["food", "culture", "affordability"],
        strengths=["Excellent value for cost", "Deep cultural and food scene", "Strong queer community presence"],
        limitations=["Safety varies significantly by district", "Traffic can affect daily quality of life"],
        score_metadata=SEED_SCORE_METADATA,
    ),
    City(
        slug="berlin-germany",
        name="Berlin",
        country="Germany",
        region="Europe",
        image="https://images.unsplash.com/photo-1560969184-10fe8719e047",
        summary="Historically important queer destination with strong inclusivity and dependable infrastructure.",
        tradeoff_summary=(
            "Berlin scores highly for inclusivity and internet, while colder weather and moderate affordability may "
            "be tradeoffs for some nomads."
        ),
        affordability=6.4,
        safety=8.2,
        internet=8.8,
        weather=5.9,
        inclusivity=9.0,
        overall_score=7.7,
        best_for=["nightlife", "queer culture", "creative work"],
        strengths=["High inclusivity signal", "Strong infrastructure and transit", "Globally recognized queer culture"],
        limitations=["Long gray winters", "Increasing accommodation costs"],
        score_metadata=SEED_SCORE_METADATA,
    ),
]


ALLOWED_SORT_FIELDS = {
    "overall_score": lambda city: city.overall_score,
    "name": lambda city: city.name.lower(),
    "affordability": lambda city: city.affordability,
    "safety": lambda city: city.safety,
    "internet": lambda city: city.internet,
    "weather": lambda city: city.weather,
    "inclusivity": lambda city: city.inclusivity,
}


@dataclass(frozen=True)
class CityDiscoveryParams:
    """Query contract for city discovery listing."""

    q: str = ""
    region: str = ""
    sort: str = "overall_score"
    min_affordability: float | None = None
    min_safety: float | None = None
    min_internet: float | None = None
    min_weather: float | None = None
    min_inclusivity: float | None = None


def get_regions() -> list[str]:
    """Return sorted unique regions available in city seed data."""
    return sorted({city.region for city in CITY_SEED_DATA})


def get_all_cities(params: CityDiscoveryParams | None = None) -> list[City]:
    """Return all cities with optional search/filter/sort discovery parameters."""
    if params is None:
        params = CityDiscoveryParams()

    filtered = CITY_SEED_DATA

    if params.q:
        normalized_query = params.q.lower()
        filtered = [
            city
            for city in filtered
            if normalized_query in city.name.lower() or normalized_query in city.country.lower()
        ]

    if params.region:
        filtered = [city for city in filtered if city.region == params.region]

    threshold_filters = [
        ("affordability", params.min_affordability),
        ("safety", params.min_safety),
        ("internet", params.min_internet),
        ("weather", params.min_weather),
        ("inclusivity", params.min_inclusivity),
    ]

    for field_name, threshold in threshold_filters:
        if threshold is not None:
            filtered = [city for city in filtered if getattr(city, field_name) >= threshold]

    sort_key = ALLOWED_SORT_FIELDS.get(params.sort, ALLOWED_SORT_FIELDS["overall_score"])
    reverse = False if params.sort == "name" else True

    return sorted(filtered, key=sort_key, reverse=reverse)


def get_city_by_slug(slug: str) -> City | None:
    """Get a single city by URL slug."""
    for city in CITY_SEED_DATA:
        if city.slug == slug:
            return city
    return None


def get_related_cities(slug: str, limit: int = 2) -> list[City]:
    """Suggest related cities using region match and score similarity."""
    city = get_city_by_slug(slug)
    if city is None:
        return []

    candidates = [candidate for candidate in CITY_SEED_DATA if candidate.slug != slug]

    def related_rank(candidate: City):
        region_bonus = 0 if candidate.region == city.region else 1
        score_distance = abs(candidate.overall_score - city.overall_score)
        return (region_bonus, score_distance, candidate.name.lower())

    return sorted(candidates, key=related_rank)[:limit]


def get_score_breakdown(city: City) -> list[tuple[str, float]]:
    """Return a normalized score breakdown list for UI rendering."""
    return [
        ("Overall", city.overall_score),
        ("Affordability", city.affordability),
        ("Safety", city.safety),
        ("Internet", city.internet),
        ("Weather", city.weather),
        ("Inclusivity", city.inclusivity),
    ]


def get_city_data_notice() -> str:
    """Shared transparency notice for city intelligence pages."""
    return (
        "City intelligence is currently based on demo seed data and heuristic scoring. "
        "Use it as directional guidance, not definitive truth."
    )


def get_methodology_content() -> dict[str, object]:
    """Methodology/trust content for city intelligence pages."""
    return {
        "score_definition": (
            "Each city score is a directional planning signal on a 0-10 scale intended to support early-stage "
            "decision making, not final relocation decisions."
        ),
        "confidence_levels": {
            "low": "Early demo/seed quality. Use for exploration only.",
            "medium": "Partially validated inputs with limited recency coverage.",
            "high": "Broad, recent, and cross-checked inputs (not yet available in this version).",
        },
        "limitations": [
            "Current dataset is seeded and intentionally small.",
            "Scores are heuristic and not authoritative measurements.",
            "Conditions can vary by neighborhood and over time.",
            "Safety and inclusivity experiences differ by identity and context.",
        ],
        "interpretation_guidance": [
            "Use scores to shortlist cities, then validate with up-to-date local research.",
            "Read score dimensions together rather than over-indexing on one metric.",
            "Treat low-confidence demo data as directional context only.",
        ],
    }
