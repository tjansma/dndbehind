"""General utility functions for the DnD Behind project."""

from flask import Response, make_response


def required_keys_present(required_keys: set[str], data: dict) -> bool:
    """Check if all required keys are present in the data dictionary.

    Args:
        required_keys (set[str]): Set of required keys.
        data (dict): Dictionary to check.

    Returns:
        bool: True if all required keys are present, False otherwise.
    """
    return required_keys.issubset(data.keys())


def make_response_without_resource_state(message: str,
                                         status_code: int) -> Response:
    """Create a JSON response with a message and status code.

    Args:
        message (str): short message describing the status of the request.
        status_code (int): HTTP status code indicating the result of the
                           request.

    Returns:
        Response: Flask Response object with JSON data.
    """
    response_dict = {
        "status": status_code,
        "msg": message
    }
    return make_response(response_dict, status_code)


def make_response_with_resource_state(message: str,
                                      status_code: int,
                                      resource_state: dict[str, str | int]
                                      ) -> Response:
    """Create a JSON response with a message, status code, and resource state.

    Args:
        message (str): short message describing the status of the request.
        status_code (int): HTTP status code indicating the result of the
                           request.
        resource_state (dict[str, str  |  int]): dictionary containing the
                                                 state of the resource.

    Returns:
        Response: Flask Response object with JSON data.
    """
    response_dict = {
        "status": status_code,
        "msg": message,
        "data": resource_state
    }
    return make_response(response_dict, status_code)
