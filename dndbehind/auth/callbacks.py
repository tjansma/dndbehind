from typing import Any

from .. import jwt
from ..models import User, db


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header: dict[str, Any],
                         jwt_data: dict[str, Any]) -> User | None:
    """User lookup callback for JWT authentication.
    This function is called by Flask-JWT-Extended to look up the user.

    Args:
        _jwt_header (dict[str, Any]): Unused argument, but required by
                                      Flask-JWT-Extended.
                                      This is the header of the JWT token.
        jwt_data (dict[str, Any]): The JWT data, which contains the user
                                   identity. This is the payload of the JWT
                                   token.

    Returns:
        User | None: The user object if found, or None if not found.
    """
    identity = jwt_data["sub"]
    return db.session.get(User, identity)
