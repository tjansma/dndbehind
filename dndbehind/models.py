"""Database models for the D&D Behind application."""

from datetime import datetime, timezone
from typing import Optional, List, TypedDict, Self, Protocol

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as orm

from . import db


# Table representing user <-> role many-to-many relationship
user_roles_table = sa.Table(
    "user_role",
    db.Model.metadata,
    sa.Column("user_id", sa.ForeignKey("user.id"), primary_key=True),
    sa.Column("role_id", sa.ForeignKey("role.id"), primary_key=True)
)


class User(UserMixin, db.Model):
    """User model for the application."""
    __table_name__ = "user"

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
    
    characters: orm.Mapped[List["Character"]] = orm.relationship(back_populates="owner")
    roles: orm.Mapped[List["Role"]] = orm.relationship(secondary=user_roles_table, back_populates="users")

    def __repr__(self) -> str:
        """Return a string representation of the user object.

        Returns:
            str: string representation of the user object
        """
        return f"<User ID {self.id} - {self.username}>"

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
        db.session.commit()

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

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "last_logged_in": self.last_logged_in,
            "disabled": self.disabled
        }

    @classmethod
    def from_id(cls, user_id: int) -> Self:
        """Construct User object from data retrieved from DB by user id.

        Args:
            user_id (int): User ID

        Raises:
            LookupError: raised when user with specified ID doesn't exist in DB.

        Returns:
            Self: constructed User object.
        """
        user = User.query.get(user_id)
        
        if not user:
            raise LookupError(f"User with ID {user_id} not found.")
        
        return user
    
    @classmethod
    def from_username(cls, username: str) -> Self:
        """Construct User object from data retrieved from DB by username.

        Args:
            username (int): Username

        Raises:
            LookupError: raised when user with specified username doesn't exist in DB.

        Returns:
            Self: constructed User object.
        """
        user = cls.query.filter(cls.username == username).first()
        
        if not user:
            raise LookupError(f"User with username '{username}' not found.")
        
        return user


class Owned(Protocol):
    owner: User


class Role(db.Model):
    """User roles for RBAC"""
    __table_name__ = "role"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String[254], nullable=False, unique=True, index=True)
    description: orm.Mapped[str] = orm.mapped_column(sa.String(1_000))

    users: orm.Mapped[List["User"]] = orm.relationship(secondary=user_roles_table, back_populates="roles")

    @classmethod
    def from_rolename(cls, rolename: str) -> Self:
        """Construct Role object from data retrieved from DB by role name.

        Args:
            rolename (str): name of role as stored in DB.

        Returns:
            Self: constructed Role object.
        """
        role = cls.query.filter(cls.name == rolename).first()

        if not role:
            raise LookupError(f"Unknown role: {rolename}")
        
        return role
    
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class CharacterDict(TypedDict):
    id: int
    name: str
    description: str
    backstory: str
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    owner_id: int
    background_id: int

class Character(db.Model):
    """D&D 5E Character model."""
    __table_name__ = "character"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(254), nullable=False, index=True)
    description: orm.Mapped[str] = orm.mapped_column(sa.String(1_000_000), nullable=True)
    backstory: orm.Mapped[str] = orm.mapped_column(sa.String(1_000_000), nullable=True)
    strength: orm.Mapped[int] = orm.mapped_column(sa.Integer(), nullable=False)
    dexterity: orm.Mapped[int] = orm.mapped_column(sa.Integer(), nullable=False)
    constitution: orm.Mapped[int] = orm.mapped_column(sa.Integer(), nullable=False)
    intelligence: orm.Mapped[int] = orm.mapped_column(sa.Integer(), nullable=False)
    wisdom: orm.Mapped[int] = orm.mapped_column(sa.Integer(), nullable=False)
    charisma: orm.Mapped[int] = orm.mapped_column(sa.Integer(), nullable=False)

    owner_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("user.id"))
    owner: orm.Mapped["User"] = orm.relationship(back_populates="characters")

    background_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("background.id"))
    background: orm.Mapped["Background"] = orm.relationship()

    def __repr__(self) -> str:
        """Return a string representation of the character object.

        Returns:
            str: string representation of the character object
        """
        return f"<Character ID {self.id} - {self.name}"
    
    def as_dict(self) -> CharacterDict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "backstory": self.backstory,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
            "owner_id": self.owner_id,
            "background_id": self.background_id
        }
    

class BackgroundDict(TypedDict):
    id: int
    name: str
    description: str

class Background(db.Model):
    """D&D 5E Background model."""
    __table_name__ = "background"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(254), nullable=False, unique=True, index=True)
    description: orm.Mapped[str] = orm.mapped_column(sa.String(100_000), nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the background object.

        Returns:
            str: string representation of the background object
        """
        return f"<Background ID {self.id} - {self.name}"
    
    def as_dict(self) -> BackgroundDict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
