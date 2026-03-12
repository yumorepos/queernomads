def apply_city_filters(cities, region=None, cost_level=None, min_score=None, sort="overall_desc"):
    filtered = cities
    if region:
        filtered = [c for c in filtered if c["region"] == region]
    if cost_level:
        filtered = [c for c in filtered if c["cost_level"] == cost_level]
    if min_score:
        filtered = [c for c in filtered if c["overall_score"] >= float(min_score)]

    reverse = sort != "overall_asc"
    filtered.sort(key=lambda city: city["overall_score"], reverse=reverse)
    return filtered
