"""Role based access control functionality."""

from functools import wraps
from typing import Callable

from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, current_user

from ..models import Owned


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


def operator_required(fn: Callable):
    """Wrapper for functions requiring operator access.

    Args:
        fn (Callable): function/endpoint requiring operator access

    Returns:
        _type_: wrapper
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        _, jwt_data = verify_jwt_in_request()

        if not _has_role(jwt_data, "operator"):
            return jsonify(msg="Operator access required."), 403
        else:
            return fn(*args, **kwargs)
        
    return wrapper


def dummy_decorator(fn: Callable):
    """Wrapper that does nothing. Can be used for interactive debugging.

    Args:
        fn (Callable): function/endpoint requiring operator access

    Returns:
        _type_: wrapper
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        _, jwt_data = verify_jwt_in_request()

        return fn(*args, **kwargs)
        
    return wrapper


def owner_or_operator_required(resource_type: type, resource_id_name: str):
    """Decorator for functions requiring either owner or operator access.
    This decorator checks if the current user is either the owner of the resource or has the operator role.

    Args:
        resource_type (type): Description of the resource type (e.g., models.Character)
        resource_id_name (str): Name of the resource ID in the request view arguments (e.g., "character_id")
    """
    def inner_decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _, jwt_data = verify_jwt_in_request()

            resource_id = request.view_args[resource_id_name]
            resource = resource_type.query.get(resource_id)
            if resource.owner == current_user or \
                    _has_role(jwt_data, "operator"):
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Owner or operator access required."), 403
            
        return wrapper
    return inner_decorator
