import json
import sqlite3
from pathlib import Path
from flask import current_app, g

ROOT = Path(__file__).resolve().parent.parent


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


def _column_exists(db, table, column):
    cols = db.execute(f"PRAGMA table_info({table})").fetchall()
    return any(col[1] == column for col in cols)


def init_db():
    db = sqlite3.connect(current_app.config["DATABASE"])
    schema_path = ROOT / "schema.sql"
    with open(schema_path, encoding="utf-8") as f:
        db.executescript(f.read())

    if not _column_exists(db, "stories", "city_id"):
        db.execute("ALTER TABLE stories ADD COLUMN city_id INTEGER REFERENCES cities(id)")

    db.commit()
    seed_db(db)
    db.close()


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

    # link legacy stories to known cities when destination matches city name
    db.execute(
        """UPDATE stories
           SET city_id = (SELECT id FROM cities WHERE LOWER(cities.name) = LOWER(stories.destination))
           WHERE city_id IS NULL"""
    )

    db.commit()
