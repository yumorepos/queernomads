from flask import Blueprint, render_template
from app.repositories.methodology_repo import get_dimensions, get_methodology_notes, get_preset_definitions

bp = Blueprint("methodology", __name__)


@bp.route("/methodology")
def methodology():
    return render_template(
        "methodology.html",
        notes=get_methodology_notes(),
        dimensions=get_dimensions(),
        presets=get_preset_definitions(),
    )
