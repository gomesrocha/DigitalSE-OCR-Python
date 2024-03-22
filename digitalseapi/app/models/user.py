"""User related data models"""
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, root_validator
from app.infra.security import HashedPassword

class User(SQLModel, table=True):
    """Represents the User Model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    password: HashedPassword = Field(nullable=False)
    name: str = Field(nullable=False)
    type: str = Field(nullable=False)

    @property
    def superuser(self):
        """"Users belonging to management dept are admins."""
        return self.type == "management"


def generate_username(name: str) -> str:
    """Generates a slug username from a name"""
    return name.lower().replace(" ", "-")


class UserResponse(BaseModel):
    """Serializer for User Response"""
    name: str
    username: str
    type: str


class UserRequest(BaseModel):
    """Serializer for User request payload"""

    name: str
    email: str
    type: str
    password: str
    username: Optional[str] = None

    @root_validator(pre=True)
    def generate_username_if_not_set(cls, values):
        """Generates username if not set"""
        if values.get("username") is None:
            values["username"] = generate_username(values["name"])
        return values