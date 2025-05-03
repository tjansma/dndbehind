"""Marshmallow schemas for Data-Transfer Objects"""
from dataclasses import dataclass

from marshmallow import fields, post_load

from . import ma
from .models import User


@dataclass
class UserCreateDTO:
    """Data Transfer Object for creating a new user."""	
    username: str
    email: str
    password: str


class UserCreateSchema(ma.SQLAlchemySchema):
    """Schema for creating a new user."""
    class Meta:
        model = User

    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

    @post_load
    def make_dto(self, data, **kwargs) -> UserCreateDTO:
        """Convert the loaded data into a UserCreateDTO instance."""
        return UserCreateDTO(**data)


# @dataclass
# class UserResponseDTO:
#     """Data Transfer Object for outputting User objects."""
#     id: int
#     username: str
#     email: str
#     last_logged_in: str
#     disabled: bool


class UserResponseSchema(ma.SQLAlchemySchema):
    """Schema for outputting user."""
    class Meta:
        model = User

    id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    last_logged_in = fields.Str(required=False)
    disabled = fields.Bool(required=True)
