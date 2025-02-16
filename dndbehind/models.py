from datetime import datetime
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as orm

from . import db


class User(UserMixin, db.Model):
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

    def __repr__(self):
        return f"<User ID {self.id} - {self.username}"

    def set_password(self, password):
        hasher = PasswordHasher()
        self.password_hash = hasher.hash(password)

    def check_password(self, password):
        hasher = PasswordHasher()
        try:
            return hasher.verify(self.password_hash, password)
        except Argon2Error:
            return False
