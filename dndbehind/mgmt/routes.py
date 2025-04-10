"""Routes for management of relatively static application data."""

from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required

from . import bp
from .. import db, models
from ..auth.rbac import role_required,  owner_or_role_required

@bp.route("/background", methods=["POST"])
@role_required("maintainer")
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
        new_background = models.Background(name=background_name,
                                           description=background_desc)
        db.session.add(new_background)
        db.session.commit()
        return jsonify(new_background.as_dict())
    except Exception as e:
        raise e


@bp.route("/background", methods=["GET"])
@role_required("maintainer")
def list_backgounds() -> str:
    """Return list with all data for all backgrounds.

    Returns:
        str: JSON document containing that list.
    """
    backgrounds = models.Background.query.all()
    return jsonify([
        background.as_dict() for background in backgrounds
    ])


@bp.route("/background/<int:background_id>", methods=["PUT"])
@role_required("maintainer")
def update_background(background_id: int) -> str:
    """Update a background.

    Args:
        background_id (int): ID of the background to update.

    Returns:
        str: JSON document with updated background data.
    """
    raise NotImplementedError("Not implemented yet.")


@bp.route("/character/<int:character_id>", methods=["GET"])
@owner_or_role_required(models.Character, "character_id", "operator")
def get_character(character_id: int) -> Response:
    """Get character data for a specific character.

    Args:
        character_id (int): ID of the character to retrieve.

    Returns:
        Response: JSON response with character data or 403 if not owner of
                  character and not operator.
    """
    return jsonify(
        { "character": models.Character.query.get(character_id).as_dict() }
    )
