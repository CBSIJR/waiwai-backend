import enum

from pydantic import BaseModel


class PermissionType(str, enum.Enum):
    GUEST = 'GUEST'
    USER = 'USER'
    ADMIN = 'ADMIN'


class Message(BaseModel):
    detail: str


class Base(BaseModel):
    id: int
