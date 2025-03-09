"""Routes for management of relatively static application data."""

from flask import request, jsonify
from flask_jwt_extended import jwt_required

from . import bp
from .. import db, models

@bp.route("/background", methods=["POST"])
@jwt_required()
def create_background() -> str:
    """Add a new D&D background.

    Raises:
        e: raised on DB error.

    Returns:
        str: JSON document with background data
    """
    background_data = request.get_json()
    background_name = background_data.get("name", None)
    background_desc = background_data.get("description", None   )

    if background_name is None or background_desc is None:
        return jsonify(msg="Background name and description required."), 400
    
    try:
        new_background = models.Background(name=background_name, description=background_desc)
        db.session.add(new_background)
        db.session.commit()
        return jsonify(new_background.as_dict())
    except Exception as e:
        raise e


@bp.route("/background", methods=["GET"])
@jwt_required()
def list_backgounds() -> str:
    """Return list with all data for all backgrounds.

    Returns:
        str: JSON document containing that list.
    """
    backgrounds = models.Background.query.all()
    return jsonify([
        background.as_dict() for background in backgrounds
    ])
