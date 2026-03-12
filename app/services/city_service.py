"""City seed data access for future intelligence features."""

from app.models.city import City


CITY_SEED_DATA = [
    City(
        name="Lisbon",
        country="Portugal",
        region="Europe",
        image="https://images.unsplash.com/photo-1585208798174-6cedd86e019a",
        affordability=7.4,
        safety=8.0,
        internet=8.5,
        weather=9.0,
        inclusivity=8.1,
        overall_score=8.2,
        best_for=["remote workers", "mild weather", "community meetups"],
        summary="Popular base with strong coworking options and a visible queer-friendly social scene.",
    ),
    City(
        name="Mexico City",
        country="Mexico",
        region="North America",
        image="https://images.unsplash.com/photo-1512813195386-6cf811ad3542",
        affordability=8.4,
        safety=6.7,
        internet=8.0,
        weather=7.8,
        inclusivity=7.6,
        overall_score=7.7,
        best_for=["food", "culture", "affordability"],
        summary="Large, dynamic city with rich queer culture and strong value for longer stays.",
    ),
    City(
        name="Berlin",
        country="Germany",
        region="Europe",
        image="https://images.unsplash.com/photo-1560969184-10fe8719e047",
        affordability=6.4,
        safety=8.2,
        internet=8.8,
        weather=5.9,
        inclusivity=9.0,
        overall_score=7.7,
        best_for=["nightlife", "queer culture", "creative work"],
        summary="Historically important queer destination with strong inclusivity and dependable infrastructure.",
    ),
]


def get_seed_cities() -> list[City]:
    """Return seed city records for planned city-intelligence features."""
    return CITY_SEED_DATA
