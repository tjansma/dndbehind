"""The management module."""

from flask import Blueprint

bp = Blueprint("mgmt", __name__)

from . import routes    # noqa: F401, E402
