from .base import Base, BaseModel

from pydantic import Field
from datetime import datetime


class WordPublic(Base):
    id: int
    word: str = Field(min_length=1, max_length=255)
    created_at: datetime
    update_at: datetime
    user_id: int


class WordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=255)


class Word(Base, WordCreate):
    user_id: int


class WordUpdate(WordCreate):
    pass
