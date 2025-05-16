from enum import Enum

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    subject: str | None = None


class PermissionEnum(str, Enum):
    admin = 'ADMIN'
    user = 'USER'
    guest = 'GUEST'


class Subject(BaseModel):
    name: str
    email: EmailStr
    permission: PermissionEnum
