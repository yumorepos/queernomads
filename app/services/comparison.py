def normalize_city_selection(requested_slugs):
    deduped = []
    seen = set()
    duplicates = []
    for slug in requested_slugs:
        if not slug:
            continue
        if slug in seen:
            duplicates.append(slug)
            continue
        seen.add(slug)
        deduped.append(slug)
    return deduped[:4], duplicates


def build_comparison_matrix(city_details):
    if not city_details:
        return []

    dimension_order = [d["key"] for d in city_details[0]["dimensions"]]
    rows = []
    for dim_key in dimension_order:
        row = {"dimension": dim_key, "label": dim_key.replace("_", " ").title(), "scores": []}
        for city in city_details:
            score = next((d for d in city["dimensions"] if d["key"] == dim_key), None)
            row["scores"].append(score["value"] if score else None)

        present = [(idx, val) for idx, val in enumerate(row["scores"]) if val is not None]
        row["winner_index"] = max(present, key=lambda x: x[1])[0] if present else None
        rows.append(row)

    return rows
