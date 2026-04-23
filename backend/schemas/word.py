from datetime import datetime
from typing import List, Optional

from pydantic import Field, field_validator

from . import ReferencePublic
from .base import Base, BaseModel, WordStatus
from .category import CategoryPublic
from .meaning import MeaningPublic
from .word_review import WordReviewPublic
from .user import UserPublic


class Word(Base):
    word: str
    phonemic: str | None
    status: WordStatus
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
    status: WordStatus
    categories: List[WordCategory]
    user: UserPublic
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
    status: WordStatus
    categories: List[WordCategory]
    attachments: List[WordAttachment]
    meanings: List[WordMeaning]
    reviews: List[WordReviewPublic]
    created_at: datetime
    updated_at: datetime


class WordExport(Base):
    word: str
    phonemic: str | None
    created_at: datetime
    updated_at: datetime
    user_id: int

class LetterStatistic(BaseModel):
    first_letter: str = Field(description="Primeira letra")
    count: int = Field(description="Quantidade total")
    percentage: float = Field(description="Porcentagem da letra")
    @field_validator("percentage")
    def format_percentage(cls, v):
        return float(f"{v:.4f}")  # enforce 4 decimal places


class WordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=100)
    phonemic: Optional[str] = Field(None, max_length=120)
    categories: List[int]


class WordUpdate(WordCreate):
    pass

