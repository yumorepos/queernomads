from app.db import get_db
from app.services.ranking_presets import PRESET_DEFINITIONS


def get_methodology_notes():
    return get_db().execute("SELECT * FROM methodology_notes ORDER BY sort_order, id").fetchall()


def get_dimensions():
    return get_db().execute("SELECT * FROM score_dimensions ORDER BY id").fetchall()


def get_preset_definitions():
    return PRESET_DEFINITIONS
