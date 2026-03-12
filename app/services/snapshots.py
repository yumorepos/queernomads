from app.services.city_scoring import CityDimensionScore, calculate_score_for_weights, summarize_tradeoffs
from app.services.ranking_presets import PRESET_DEFINITIONS


def rebuild_city_snapshots(db):
    city_rows = db.execute("SELECT id FROM cities ORDER BY id").fetchall()
    for city in city_rows:
        dims = _load_city_dimensions(db, city["id"])
        if not dims:
            continue

        strengths, tradeoffs = summarize_tradeoffs(dims)
        scores = {
            key: calculate_score_for_weights(dims, preset["weights"])
            for key, preset in PRESET_DEFINITIONS.items()
        }

        db.execute(
            """INSERT INTO city_snapshots
            (city_id, overall_score, balanced_score, remote_work_score, community_score, strengths, tradeoffs, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(city_id)
            DO UPDATE SET
                overall_score = excluded.overall_score,
                balanced_score = excluded.balanced_score,
                remote_work_score = excluded.remote_work_score,
                community_score = excluded.community_score,
                strengths = excluded.strengths,
                tradeoffs = excluded.tradeoffs,
                updated_at = excluded.updated_at""",
            (
                city["id"],
                scores["balanced"],
                scores["balanced"],
                scores["best_for_remote_work"],
                scores["best_for_community"],
                ", ".join(strengths),
                ", ".join(tradeoffs),
            ),
        )

    db.commit()


def _load_city_dimensions(db, city_id):
    rows = db.execute(
        """SELECT sd.key, sd.label, sd.weight_default, cs.score, cs.evidence_note, cs.source_count, cs.confidence
        FROM city_scores cs JOIN score_dimensions sd ON sd.id = cs.dimension_id
        WHERE cs.city_id = ?""",
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
