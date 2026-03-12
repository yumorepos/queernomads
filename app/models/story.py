"""Story model helpers for typed route/service boundaries."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StoryCategory:
    """Allowed story categories used in forms and validation."""

    value: str


VALID_STORY_CATEGORIES = (
    "nightlife",
    "safety",
    "community",
    "accommodation",
    "general",
)
