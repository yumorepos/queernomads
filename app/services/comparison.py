def build_comparison_matrix(city_details):
    if not city_details:
        return []

    dimension_order = [d["key"] for d in city_details[0]["dimensions"]]
    rows = []
    for dim_key in dimension_order:
        row = {"dimension": dim_key, "scores": []}
        for city in city_details:
            score = next((d for d in city["dimensions"] if d["key"] == dim_key), None)
            row["scores"].append(score["value"] if score else None)
        rows.append(row)
    return rows
