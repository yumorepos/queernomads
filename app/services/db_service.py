"""Database lifecycle and query helpers."""

from pathlib import Path
import sqlite3

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    """Get request-scoped database connection."""
    if "db" not in g:
        db_path = current_app.config["DATABASE"]
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exception=None) -> None:
    """Close request-scoped database connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Initialize database tables from schema.sql if not present."""
    db_path = Path(current_app.config["DATABASE"])
    schema_path = Path(current_app.config["SCHEMA_PATH"])

    db = sqlite3.connect(db_path)
    with schema_path.open() as schema_file:
        db.executescript(schema_file.read())
    db.close()


def get_user_by_id(user_id: int):
    """Fetch a single user row by id."""
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
