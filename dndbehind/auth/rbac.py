"""Role based access control functionality."""

from functools import wraps
from typing import Callable

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request


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

        if "roles" not in jwt_data or "admin" not in jwt_data["roles"]:
            return jsonify(msg="Administrative access required."), 403
        else:
            return fn(*args, **kwargs)
        
    return wrapper
