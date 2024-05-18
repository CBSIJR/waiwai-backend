import enum

from pydantic import BaseModel


class WordCategoryExport(BaseModel):
    word_id: int
    category_id: int


class PermissionType(str, enum.Enum):
    GUEST = 'GUEST'
    USER = 'USER'
    ADMIN = 'ADMIN'


class Message(BaseModel):
    detail: str


class Base(BaseModel):
    id: int
