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


def calculate_score_for_weights(dimension_scores, weights):
    weighted_pairs = [
        (d.value, weights.get(d.key, d.weight_default))
        for d in dimension_scores
    ]
    total_weight = sum(weight for _, weight in weighted_pairs) or 1
    weighted_sum = sum(value * weight for value, weight in weighted_pairs)
    return round(weighted_sum / total_weight, 1)


def calculate_overall_score(dimension_scores):
    return calculate_score_for_weights(
        dimension_scores,
        {d.key: d.weight_default for d in dimension_scores},
    )


def summarize_tradeoffs(dimension_scores):
    ordered = sorted(dimension_scores, key=lambda d: (d.value, d.label), reverse=True)
    strengths = [f"{d.label} ({int(d.value)})" for d in ordered[:2]]
    tradeoffs = [f"{d.label} ({int(d.value)})" for d in ordered[-2:]]
    return strengths, tradeoffs
