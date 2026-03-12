from app.services.city_scoring import CityDimensionScore, calculate_overall_score, summarize_tradeoffs
from app.services.comparison import build_comparison_matrix


def test_calculate_overall_score_weighted():
    dims = [
        CityDimensionScore("a", "A", 80, 1.0, "", 1, "medium"),
        CityDimensionScore("b", "B", 60, 2.0, "", 1, "medium"),
    ]
    assert calculate_overall_score(dims) == 66.7


def test_tradeoff_summary():
    dims = [
        CityDimensionScore("a", "A", 80, 1.0, "", 1, "medium"),
        CityDimensionScore("b", "B", 60, 1.0, "", 1, "medium"),
        CityDimensionScore("c", "C", 40, 1.0, "", 1, "medium"),
    ]
    strengths, tradeoffs = summarize_tradeoffs(dims)
    assert strengths[0].startswith("A")
    assert tradeoffs[-1].startswith("C")


def test_comparison_matrix():
    matrix = build_comparison_matrix([
        {"dimensions": [{"key": "safety", "value": 80}, {"key": "cost", "value": 60}]},
        {"dimensions": [{"key": "safety", "value": 70}, {"key": "cost", "value": 90}]},
    ])
    assert matrix[0]["dimension"] == "safety"
    assert matrix[1]["scores"][1] == 90
