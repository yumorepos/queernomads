SORT_OPTIONS = {"score_desc", "score_asc", "name_asc"}


def apply_city_filters(cities, region=None, cost_level=None, min_score=None, sort="score_desc"):
    filtered = list(cities)

    if region:
        filtered = [c for c in filtered if c["region"] == region]
    if cost_level:
        filtered = [c for c in filtered if c["cost_level"] == cost_level]

    min_score_value = _safe_float(min_score)
    if min_score_value is not None:
        filtered = [c for c in filtered if c["active_score"] >= min_score_value]

    sort_key = sort if sort in SORT_OPTIONS else "score_desc"
    if sort_key == "score_asc":
        filtered.sort(key=lambda city: (city["active_score"], city["name"]))
    elif sort_key == "name_asc":
        filtered.sort(key=lambda city: city["name"])
    else:
        filtered.sort(key=lambda city: (-city["active_score"], city["name"]))

    return filtered


def _safe_float(value):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
