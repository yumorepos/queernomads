from app.services.city_scoring import CityDimensionScore, calculate_score_for_weights, summarize_tradeoffs
from app.services.comparison import build_comparison_matrix, normalize_city_selection
from app.services.ranking_presets import PRESET_DEFINITIONS


def test_calculate_score_with_custom_weights():
    dims = [
        CityDimensionScore("internet", "Internet", 80, 1.0, "", 1, "medium"),
        CityDimensionScore("community", "Community", 60, 1.0, "", 1, "medium"),
    ]
    score = calculate_score_for_weights(dims, {"internet": 2.0, "community": 1.0})
    assert score == 73.3


def test_preset_weights_are_distinct():
    assert PRESET_DEFINITIONS["balanced"]["weights"] != PRESET_DEFINITIONS["best_for_remote_work"]["weights"]


def test_tradeoff_summary():
    dims = [
        CityDimensionScore("a", "A", 80, 1.0, "", 1, "medium"),
        CityDimensionScore("b", "B", 60, 1.0, "", 1, "medium"),
        CityDimensionScore("c", "C", 40, 1.0, "", 1, "medium"),
    ]
    strengths, tradeoffs = summarize_tradeoffs(dims)
    assert strengths[0].startswith("A")
    assert tradeoffs[-1].startswith("C")


def test_compare_normalization_and_matrix():
    slugs, duplicates = normalize_city_selection(["lisbon", "lisbon", "berlin", "", "bangkok"])
    assert slugs == ["lisbon", "berlin", "bangkok"]
    assert duplicates == ["lisbon"]

    matrix = build_comparison_matrix([
        {"dimensions": [{"key": "safety", "value": 80}, {"key": "cost", "value": 60}]},
        {"dimensions": [{"key": "safety", "value": 70}, {"key": "cost", "value": 90}]},
    ])
    assert matrix[0]["dimension"] == "safety"
    assert matrix[1]["scores"][1] == 90
    assert matrix[0]["winner_index"] == 0
