import sqlite3
from pathlib import Path

from app import create_app
from app.db import run_migrations


def test_migrations_apply_versions(tmp_path: Path):
    db_path = tmp_path / "migration_test.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    run_migrations(conn)

    versions = {row["version"] for row in conn.execute("SELECT version FROM schema_migrations").fetchall()}
    assert "001_initial" in versions
    assert "002_snapshot_preset_scores" in versions

    cols = conn.execute("PRAGMA table_info(city_snapshots)").fetchall()
    col_names = {col[1] for col in cols}
    assert {"balanced_score", "remote_work_score", "community_score"}.issubset(col_names)


def test_snapshot_read_model_populated():
    app = create_app({"TESTING": True, "DATABASE": "test_qn.db"})
    with app.app_context():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        snapshot = conn.execute("SELECT * FROM city_snapshots WHERE city_id = (SELECT id FROM cities WHERE slug = 'lisbon')").fetchone()
        assert snapshot is not None
        assert snapshot["balanced_score"] is not None
        assert snapshot["remote_work_score"] is not None
        assert snapshot["community_score"] is not None
        conn.close()
