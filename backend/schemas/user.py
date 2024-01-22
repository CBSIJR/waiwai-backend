from pydantic import BaseModel, EmailStr
from .base import Base


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class User(Base, UserCreate):
    pass


class UserUpdate(UserCreate):
    pass


class UserList(BaseModel):
    users: list[UserPublic]
