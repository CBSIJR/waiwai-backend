from datetime import datetime

from pydantic import Field

from .base import Base, BaseModel
from .category import CategoryPublic
from .meaning import MeaningPublic


class WordPublic(Base):
    id: int
    word: str
    created_at: datetime
    update_at: datetime
    categories: list[CategoryPublic]
    meanings: list[MeaningPublic]
    user_id: int


class WordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=50)
    categories: list[int]


class Word(Base, WordCreate):
    user_id: int


class WordUpdate(WordCreate):
    pass
