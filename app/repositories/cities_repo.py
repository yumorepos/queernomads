from app.db import get_db
from app.services.city_scoring import CityDimensionScore, summarize_tradeoffs

SNAPSHOT_SCORE_COLUMN = {
    "balanced": "balanced_score",
    "best_for_remote_work": "remote_work_score",
    "best_for_community": "community_score",
}


def list_cities_with_scores(preset="balanced"):
    db = get_db()
    score_column = SNAPSHOT_SCORE_COLUMN.get(preset, "balanced_score")
    rows = db.execute(
        f"""SELECT c.*, cs.overall_score, cs.balanced_score, cs.remote_work_score, cs.community_score,
               cs.strengths, cs.tradeoffs,
               cs.{score_column} AS active_score
           FROM cities c
           JOIN city_snapshots cs ON cs.city_id = c.id
           ORDER BY c.name"""
    ).fetchall()

    return [_city_summary_from_row(row, preset) for row in rows]


def get_city_by_slug(slug):
    db = get_db()
    city = db.execute("SELECT * FROM cities WHERE slug = ?", (slug,)).fetchone()
    if not city:
        return None

    snapshot = db.execute("SELECT * FROM city_snapshots WHERE city_id = ?", (city["id"],)).fetchone()
    dimensions = _get_city_dimensions(city["id"])

    if snapshot:
        strengths = snapshot["strengths"].split(", ") if snapshot["strengths"] else []
        tradeoffs = snapshot["tradeoffs"].split(", ") if snapshot["tradeoffs"] else []
    else:
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
        "overall_score": snapshot["overall_score"] if snapshot else None,
        "balanced_score": snapshot["balanced_score"] if snapshot else None,
        "remote_work_score": snapshot["remote_work_score"] if snapshot else None,
        "community_score": snapshot["community_score"] if snapshot else None,
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


def list_regions():
    rows = get_db().execute("SELECT DISTINCT region FROM cities ORDER BY region").fetchall()
    return [r["region"] for r in rows]


def _get_city_dimensions(city_id):
    rows = get_db().execute(
        """SELECT sd.key, sd.label, sd.weight_default, cs.score, cs.evidence_note, cs.source_count, cs.confidence
           FROM city_scores cs
           JOIN score_dimensions sd ON sd.id = cs.dimension_id
           WHERE cs.city_id = ?
           ORDER BY sd.id""",
        (city_id,),
    ).fetchall()

    return [
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


def _city_summary_from_row(row, preset):
    return {
        "id": row["id"],
        "slug": row["slug"],
        "name": row["name"],
        "country": row["country"],
        "region": row["region"],
        "summary": row["summary"],
        "cost_level": row["cost_level"],
        "confidence": row["confidence"],
        "overall_score": row["overall_score"],
        "active_score": row["active_score"],
        "preset": preset,
        "strengths": row["strengths"].split(", ") if row["strengths"] else [],
        "tradeoffs": row["tradeoffs"].split(", ") if row["tradeoffs"] else [],
    }
