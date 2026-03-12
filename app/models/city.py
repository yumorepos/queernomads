"""City domain model for city-intelligence features."""

from dataclasses import dataclass, field
from datetime import date
from typing import Literal


ConfidenceLabel = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class CityScoreMetadata:
    """Metadata that explains where city scores came from and how reliable they are."""

    source_name: str
    source_url: str
    methodology_note: str
    confidence_label: ConfidenceLabel
    last_reviewed: date
    is_demo_data: bool = True


@dataclass(frozen=True)
class City:
    """Represents a city profile in the city-intelligence dataset."""

    slug: str
    name: str
    country: str
    region: str
    image: str
    summary: str
    affordability: float
    safety: float
    internet: float
    weather: float
    inclusivity: float
    overall_score: float
    best_for: list[str] = field(default_factory=list)
    score_metadata: CityScoreMetadata = field(
        default_factory=lambda: CityScoreMetadata(
            source_name="QueerNomads seed dataset",
            source_url="https://github.com/yumorepos/queernomads",
            methodology_note="Seed/demo values for product prototyping.",
            confidence_label="low",
            last_reviewed=date.today(),
            is_demo_data=True,
        )
    )

    @property
    def transparency_label(self) -> str:
        """Human-readable data transparency label."""
        if self.score_metadata.is_demo_data:
            return "Demo intelligence (seed data)"
        return f"{self.score_metadata.confidence_label.title()} confidence"
