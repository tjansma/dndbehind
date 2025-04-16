"""Role based access control functionality."""

from functools import wraps
from typing import Callable

from flask import Response, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, current_user

from ..models import User


def _has_role(jwt_data: dict, role_name: str) -> bool:
    """Check of JWT data contains roles, and if so, if the specified role is
    contained.

    Args:
        jwt_data (dict): JSON Web Token data as a dictionary
        role_name (str): unique name of the role to check for

    Returns:
        bool: True if specified role is in jwt_data, False otherwise
    """
    return "roles" in jwt_data and role_name in jwt_data["roles"]


def self_or_role_required(user_id_arg_name: str, *role_names: str) -> Callable:
    """Decorator for functions requiring either self or role-based access.
    This decorator checks if the current user is either the target user or has
    one of the specified roles.

    Args:
        user_id_arg_name (str): Name of the user ID in the request view
                                arguments (e.g., "user_id")
        role_names (str): Names of the roles to check for (e.g., "admin",
                          "operator")
    """
    def inner_decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _, jwt_data = verify_jwt_in_request()

            target_user = User.from_id(request.view_args[user_id_arg_name])
            if target_user == current_user:
                return fn(*args, **kwargs)

            for role_name in role_names:
                if _has_role(jwt_data, role_name):
                    return fn(*args, **kwargs)

            return jsonify(msg="Access denied."), 403

        return wrapper
    return inner_decorator


def owner_or_role_required(resource_type: type,
                           resource_id_arg_name: str,
                           *role_names: str) -> Callable:
    """Decorator for functions requiring either owner or role-based access.
    This decorator checks if the current user is either the owner of the
    resource or has one of the specified roles.

    Args:
        resource_type (type): Description of the resource type
                              (e.g., models.Character)
        resource_id_arg_name (str): Name of the resource ID in the request view
                                    arguments (e.g., "character_id")
        role_names (str): Names of the roles to check for (e.g., "admin",
                          "operator")
    """
    def inner_decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _, jwt_data = verify_jwt_in_request()

            resource_id = request.view_args[resource_id_arg_name]
            resource = resource_type.query.get(resource_id)
            if resource.owner == current_user:
                return fn(*args, **kwargs)

            for role_name in role_names:
                if _has_role(jwt_data, role_name):
                    return fn(*args, **kwargs)

            return jsonify(msg="Access denied."), 403

        return wrapper
    return inner_decorator


def role_required(*role_names: str) -> Callable:
    """Decorator for functions requiring (a) specific role(s).
    This decorator checks if the current user has one of the specified roles.

    Args:
        role_names (str): Names of the roles to check for (e.g., "admin",
                          "operator")
    """
    def inner_decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Callable | Response:
            _, jwt_data = verify_jwt_in_request()

            for role_name in role_names:
                if _has_role(jwt_data, role_name):
                    return fn(*args, **kwargs)

            return jsonify(msg="Access denied."), 403
        return wrapper
    return inner_decorator
