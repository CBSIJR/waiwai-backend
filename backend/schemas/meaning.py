from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .base import Base


class Meaning(Base):
    meaning_pt: str
    meaning_ww: str | None
    comment_pt: str | None
    comment_ww: str | None
    created_at: datetime
    updated_at: datetime
    word_id: int
    reference_id: int
    user_id: int


class MeaningExport(Meaning):
    pass


class MeaningPublic(Meaning):
    pass


class MeaningCreate(BaseModel):
    meaning_pt: str = Field(min_length=1, max_length=300)
    meaning_ww: Optional[str] = Field(min_length=1, max_length=300)
    comment_ww: Optional[str] = Field(min_length=5, max_length=800)
    comment_pt: Optional[str] = Field(min_length=5, max_length=800)
    reference_id: int = Field(min=1)


class MeaningUpdate(MeaningCreate):
    pass
