from datetime import datetime
from typing import List, Optional

from pydantic import Field

from . import ReferencePublic
from .base import Base, BaseModel
from .category import CategoryPublic
from .meaning import MeaningPublic


class Word(Base):
    word: str
    phonemic: str | None
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryPublic]
    meanings: List[MeaningPublic]
    user_id: int


class WordCategory(BaseModel):
    id: int
    category: str
    model_config = {'from_attributes': True}


class WordPublic(Base):
    word: str
    phonemic: str | None
    categories: List[WordCategory]
    created_at: datetime
    updated_at: datetime


class WordAttachment(Base):
    url: str
    content_type: str
    created_at: datetime


class WordMeaning(Base):
    meaning_pt: str
    meaning_ww: str | None
    comment_pt: str | None
    comment_ww: str | None
    created_at: datetime
    updated_at: datetime
    reference: ReferencePublic


class WordDetails(Base):
    word: str
    phonemic: str | None
    categories: List[WordCategory]
    attachments: List[WordAttachment]
    meanings: List[WordMeaning]
    created_at: datetime
    updated_at: datetime


class WordExport(Base):
    word: str
    phonemic: str | None
    created_at: datetime
    updated_at: datetime
    user_id: int


class WordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=100)
    phonemic: Optional[str] = Field(min_length=1, max_length=120)
    categories: List[int]


class WordUpdate(WordCreate):
    pass
