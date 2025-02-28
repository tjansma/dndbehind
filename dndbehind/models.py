"""Database models for the D&D Behind application."""

from datetime import datetime, timezone
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as orm

from . import db


class User(UserMixin, db.Model):
    """User model for the application."""
    id: orm.Mapped[int] = orm.mapped_column(
        primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(
        sa.String(254),
        index=True,
        unique=True)
    email: orm.Mapped[str] = orm.mapped_column(
        sa.String(254),
        index=True,
        unique=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(
        sa.String(256))
    last_logged_in: orm.Mapped[Optional[datetime]] = orm.mapped_column(
        sa.DateTime())
    disabled: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean(),
        default=False)

    def __repr__(self) -> str:
        """Return a string representation of the user object.

        Returns:
            str: string representation of the user object
        """
        return f"<User ID {self.id} - {self.username}"

    def set_password(self, password: str) -> None:
        """Sets the password hash for the user.

        Args:
            password (str): the password to hash
        """
        hasher = PasswordHasher()
        self.password_hash = hasher.hash(password)

    def check_password(self, password: str) -> bool:
        """Check the password against the stored hash.

        Args:
            password (str): the password to check

        Returns:
            bool: True if the password matches the stored hash, False otherwise
        """
        hasher = PasswordHasher()
        try:
            return hasher.verify(self.password_hash, password)
        except Argon2Error:
            return False

    def update_login_time(self) -> None:
        """Update the last logged in time to the current time."""
        self.last_logged_in = datetime.now(timezone.utc)

    def is_disabled(self) -> bool:
        """Check if the user is disabled.

        Returns:
            bool: True if the user is disabled, False otherwise
        """
        return self.disabled
    
    def set_disabled(self, disabled: bool) -> None:
        """Set the disabled status of the user.

        Args:
            disabled (bool): the disabled status to set
        """
        self.disabled = disabled
