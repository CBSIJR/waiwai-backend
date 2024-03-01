from typing import Optional

from pydantic import BaseModel, Field

from .base import Base


class Meaning(Base):
    meaning: str
    phonemic: str | None
    comment: str | None
    chapter_id: int | None
    entry_id: int | None
    reference_id: int


class MeaningPublic(Meaning):
    pass


class MeaningCreate(BaseModel):
    meaning: str = Field(min_length=1, max_length=200)
    phonemic: Optional[str] = Field(min_length=1, max_length=120)
    comment: Optional[str] = Field(min_length=5, max_length=256)
    chapter_id: Optional[int]
    entry_id: Optional[int]
    reference_id: int


class MeaningUpdate(MeaningCreate):
    pass
