from dataclasses import dataclass


@dataclass
class CityDimensionScore:
    key: str
    label: str
    value: float
    weight_default: float
    evidence_note: str
    source_count: int
    confidence: str


def calculate_overall_score(dimension_scores):
    total_weight = sum(d.weight_default for d in dimension_scores) or 1
    weighted_sum = sum(d.value * d.weight_default for d in dimension_scores)
    return round(weighted_sum / total_weight, 1)


def summarize_tradeoffs(dimension_scores):
    ordered = sorted(dimension_scores, key=lambda d: d.value, reverse=True)
    strengths = [f"{d.label} ({int(d.value)})" for d in ordered[:2]]
    tradeoffs = [f"{d.label} ({int(d.value)})" for d in ordered[-2:]]
    return strengths, tradeoffs
