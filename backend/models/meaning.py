from __future__ import annotations
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .word import Word
    from .word import Word
    from .reference import Reference
else:
    Word = "Word"

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql.functions import func

from .base import Base

from datetime import datetime


class Meaning(Base):
    __tablename__ = 'meanings'

    id: Mapped[int] = mapped_column(primary_key=True)
    meaning: Mapped[str] = mapped_column(String(50))
    phonemic: Mapped[str] = mapped_column(String(80))
    comment: Mapped[str] = mapped_column(String(255))
    chapter_id: Mapped[Optional[int]]
    entry_id: Mapped[Optional[int]]
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          onupdate=func.now())
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    word: Mapped[Word] = relationship(back_populates="meanings")

    reference_id: Mapped[int] = mapped_column(ForeignKey("references.id"))
    reference: Mapped[Reference] = relationship(back_populates="meanings")
