from app.db import get_db


def get_methodology_notes():
    return get_db().execute("SELECT * FROM methodology_notes ORDER BY sort_order, id").fetchall()


def get_dimensions():
    return get_db().execute("SELECT * FROM score_dimensions ORDER BY id").fetchall()
