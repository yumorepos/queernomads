"""Application factory for QueerNomads."""

import os
from pathlib import Path

from flask import Flask, session

from app.routes.city_routes import city_bp
from app.routes.main_routes import main_bp
from app.routes.story_routes import story_bp
from app.services.db_service import close_db, get_user_by_id, init_db


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DEV_SECRET = "queernomads-dev-secret-key-change-in-production"


def create_app() -> Flask:
    """Create and configure Flask app instance."""
    flask_app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    flask_app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", DEFAULT_DEV_SECRET)
    flask_app.config["DATABASE"] = str(BASE_DIR / "queernomads.db")
    flask_app.config["SCHEMA_PATH"] = str(BASE_DIR / "schema.sql")

    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(story_bp)
    flask_app.register_blueprint(city_bp)

    flask_app.teardown_appcontext(close_db)

    @flask_app.context_processor
    def inject_user():
        """Make current user available to all templates."""
        if session.get("user_id"):
            user = get_user_by_id(session["user_id"])
            return {"current_user": user}
        return {"current_user": None}

    with flask_app.app_context():
        init_db()

    return flask_app
