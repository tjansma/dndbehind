"""The auth module."""

from flask import Blueprint

bp = Blueprint("auth", __name__)

from . import routes        # noqa: F401, E402
from . import callbacks     # noqa: F401, E402
