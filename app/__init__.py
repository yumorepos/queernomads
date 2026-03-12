import click
from flask import Flask, session

from .config import Config
from .db import close_db, get_db, init_app_data


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)

    @app.context_processor
    def inject_user():
        if session.get("user_id"):
            user = get_db().execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
            return {"current_user": user}
        return {"current_user": None}

    @app.cli.command("migrate")
    def migrate_command():
        """Apply database migrations and refresh snapshots."""
        with app.app_context():
            init_app_data()
        click.echo("Migrations + seeds + snapshots completed.")

    from .routes import auth, cities, compare, community, main, methodology

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(community.bp)
    app.register_blueprint(cities.bp)
    app.register_blueprint(compare.bp)
    app.register_blueprint(methodology.bp)

    with app.app_context():
        init_app_data()

    return app
