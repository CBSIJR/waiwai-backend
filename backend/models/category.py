from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .word import Word
else:
    Word = 'Word'

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, WordCategory


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(20), unique=True)
    description: Mapped[str] = mapped_column(String(255))

    words: Mapped[Optional[List[Word]]] = relationship(
        secondary=WordCategory, back_populates='categories'
    )
