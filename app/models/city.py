"""City domain model for future city-intelligence features."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class City:
    """Represents a city profile in the city-intelligence dataset."""

    name: str
    country: str
    region: str
    image: str
    affordability: float
    safety: float
    internet: float
    weather: float
    inclusivity: float
    overall_score: float
    best_for: list[str] = field(default_factory=list)
    summary: str = ""
