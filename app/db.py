import json
import sqlite3
from pathlib import Path
from flask import current_app, g

from app.services.snapshots import rebuild_city_snapshots

ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = ROOT / "migrations"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app_data():
    db = sqlite3.connect(current_app.config["DATABASE"])
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    run_migrations(db)
    seed_db(db)
    rebuild_city_snapshots(db)
    db.close()


def run_migrations(db):
    db.execute(
        """CREATE TABLE IF NOT EXISTS schema_migrations (
           version TEXT PRIMARY KEY,
           applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    applied = {row["version"] for row in db.execute("SELECT version FROM schema_migrations").fetchall()}
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    for path in migration_files:
        version = path.stem
        if version in applied:
            continue

        script = path.read_text(encoding="utf-8")
        try:
            db.executescript(script)
        except sqlite3.OperationalError as exc:
            if _can_ignore_column_exists_error(db, version, str(exc)):
                pass
            else:
                raise

        db.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))
        db.commit()


def _can_ignore_column_exists_error(db, version, error):
    if version != "002_snapshot_preset_scores":
        return False
    expected = {
        "balanced_score": _column_exists(db, "city_snapshots", "balanced_score"),
        "remote_work_score": _column_exists(db, "city_snapshots", "remote_work_score"),
        "community_score": _column_exists(db, "city_snapshots", "community_score"),
    }
    if all(expected.values()):
        return "duplicate column name" in error.lower()
    return False


def _column_exists(db, table, column):
    cols = db.execute(f"PRAGMA table_info({table})").fetchall()
    return any(col[1] == column for col in cols)


def seed_db(db):
    city_count = db.execute("SELECT COUNT(*) FROM cities").fetchone()[0]
    if city_count == 0:
        cities = json.loads((ROOT / "data/seed/cities.json").read_text(encoding="utf-8"))
        for city in cities:
            db.execute(
                """INSERT INTO cities
                (slug, name, country, region, summary, queer_nomad_note, cost_level, timezone, hero_image, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    city["slug"],
                    city["name"],
                    city["country"],
                    city["region"],
                    city["summary"],
                    city["queer_nomad_note"],
                    city["cost_level"],
                    city["timezone"],
                    city.get("hero_image", ""),
                    city.get("confidence", "medium"),
                ),
            )

    dim_count = db.execute("SELECT COUNT(*) FROM score_dimensions").fetchone()[0]
    if dim_count == 0:
        payload = json.loads((ROOT / "data/seed/scores.json").read_text(encoding="utf-8"))
        for dim in payload["dimensions"]:
            db.execute(
                "INSERT INTO score_dimensions (key, label, description, weight_default) VALUES (?, ?, ?, ?)",
                (dim["key"], dim["label"], dim["description"], dim["weight_default"]),
            )

        for score in payload["scores"]:
            city_id = db.execute("SELECT id FROM cities WHERE slug = ?", (score["city_slug"],)).fetchone()[0]
            dim_id = db.execute("SELECT id FROM score_dimensions WHERE key = ?", (score["dimension_key"],)).fetchone()[0]
            db.execute(
                """INSERT INTO city_scores
                (city_id, dimension_id, score, evidence_note, source_count, confidence, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (city_id, dim_id, score["score"], score["evidence_note"], score["source_count"], score["confidence"]),
            )

    method_count = db.execute("SELECT COUNT(*) FROM methodology_notes").fetchone()[0]
    if method_count == 0:
        notes = json.loads((ROOT / "data/seed/methodology.json").read_text(encoding="utf-8"))
        for note in notes:
            db.execute(
                "INSERT INTO methodology_notes (section, body, sort_order) VALUES (?, ?, ?)",
                (note["section"], note["body"], note["sort_order"]),
            )

    db.execute(
        """UPDATE stories
           SET city_id = (SELECT id FROM cities WHERE LOWER(cities.name) = LOWER(stories.destination))
           WHERE city_id IS NULL"""
    )

    db.commit()
