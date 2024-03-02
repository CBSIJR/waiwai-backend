from datetime import datetime
from typing import List, Optional

from pydantic import Field

from .base import Base, BaseModel
from .category import CategoryPublic
from .meaning import MeaningPublic


class Word(Base):
    word: str
    phonemic: str | None
    created_at: datetime
    update_at: datetime
    categories: List[CategoryPublic]
    meanings: List[MeaningPublic]
    user_id: int


class WordPublic(Word):
    pass


class WordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=50)
    phonemic: Optional[str] = Field(min_length=1, max_length=120)
    categories: List[int]


class WordUpdate(WordCreate):
    pass
