"""Role based access control functionality."""

from functools import wraps
from typing import Callable

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request


def _has_role(jwt_data: dict, role_name: str) -> bool:
    """Check of JWT data contains roles, and if so, if the specified role is contained.

    Args:
        jwt_data (dict): JSON Web Token data as a dictionary
        role_name (str): unique name of the role to check for

    Returns:
        bool: True if specified role is in jwt_data, False otherwise
    """
    return "roles" in jwt_data and role_name in jwt_data["roles"]


def admin_required(fn: Callable):
    """Wrapper for functions requiring administrative access.

    Args:
        fn (Callable): function/endpoint requiring administrative access

    Returns:
        _type_: wrapper
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        _, jwt_data = verify_jwt_in_request()

        if not _has_role(jwt_data, "admin"):
            return jsonify(msg="Administrative access required."), 403
        else:
            return fn(*args, **kwargs)
        
    return wrapper


def maintainer_required(fn: Callable):
    """Wrapper for functions requiring maintainer access.

    Args:
        fn (Callable): function/endpoint requiring maintenance access

    Returns:
        _type_: wrapper
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        _, jwt_data = verify_jwt_in_request()

        if not _has_role(jwt_data, "maintainer"):
            return jsonify(msg="Maintenance access required."), 403
        else:
            return fn(*args, **kwargs)
        
    return wrapper
