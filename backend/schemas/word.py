from datetime import datetime

from pydantic import Field

from .base import Base, BaseModel
from .category import CategoryPublic


class WordPublic(Base):
    id: int
    word: str = Field(min_length=1, max_length=255)
    created_at: datetime
    update_at: datetime
    categories: list[CategoryPublic]
    user_id: int


class WordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=255)
    categories: list[int]


class Word(Base, WordCreate):
    user_id: int


class WordUpdate(WordCreate):
    pass
