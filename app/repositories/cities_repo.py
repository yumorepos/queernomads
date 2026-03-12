from app.db import get_db
from app.services.city_scoring import CityDimensionScore, calculate_overall_score, summarize_tradeoffs


def list_cities_with_scores():
    db = get_db()
    cities = db.execute("SELECT * FROM cities ORDER BY name").fetchall()
    return [_hydrate_city(city["slug"]) for city in cities]


def get_city_by_slug(slug):
    return _hydrate_city(slug)


def list_regions():
    rows = get_db().execute("SELECT DISTINCT region FROM cities ORDER BY region").fetchall()
    return [r["region"] for r in rows]


def _hydrate_city(slug):
    db = get_db()
    city = db.execute("SELECT * FROM cities WHERE slug = ?", (slug,)).fetchone()
    if not city:
        return None

    rows = db.execute(
        """SELECT sd.key, sd.label, sd.weight_default, cs.score, cs.evidence_note, cs.source_count, cs.confidence
           FROM city_scores cs
           JOIN score_dimensions sd ON sd.id = cs.dimension_id
           WHERE cs.city_id = ?
           ORDER BY sd.id""",
        (city["id"],),
    ).fetchall()

    dimensions = [
        CityDimensionScore(
            key=r["key"],
            label=r["label"],
            value=r["score"],
            weight_default=r["weight_default"],
            evidence_note=r["evidence_note"],
            source_count=r["source_count"],
            confidence=r["confidence"],
        )
        for r in rows
    ]

    overall = calculate_overall_score(dimensions)
    strengths, tradeoffs = summarize_tradeoffs(dimensions)
    return {
        "id": city["id"],
        "slug": city["slug"],
        "name": city["name"],
        "country": city["country"],
        "region": city["region"],
        "summary": city["summary"],
        "queer_nomad_note": city["queer_nomad_note"],
        "cost_level": city["cost_level"],
        "timezone": city["timezone"],
        "confidence": city["confidence"],
        "overall_score": overall,
        "strengths": strengths,
        "tradeoffs": tradeoffs,
        "dimensions": [
            {
                "key": d.key,
                "label": d.label,
                "value": d.value,
                "weight_default": d.weight_default,
                "evidence_note": d.evidence_note,
                "source_count": d.source_count,
                "confidence": d.confidence,
            }
            for d in dimensions
        ],
    }
