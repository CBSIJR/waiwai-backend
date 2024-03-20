from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .reference import Reference
    from .user import User
    from .word import Word
else:
    Word = 'Word'
    User = 'User'
    Reference = 'Reference'

from datetime import datetime

from sqlalchemy import  DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func

from .base import Base


class Meaning(Base):
    __tablename__ = 'meanings'

    id: Mapped[int] = mapped_column(primary_key=True)
    meaning: Mapped[str] = mapped_column(String(200))
    comment: Mapped[Optional[str]] = mapped_column(String(256))
    chapter_id: Mapped[Optional[int]]
    entry_id: Mapped[Optional[int]]
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(back_populates='meanings')

    word_id: Mapped[int] = mapped_column(ForeignKey('words.id'))
    word: Mapped[Word] = relationship(back_populates='meanings')

    reference_id: Mapped[int] = mapped_column(ForeignKey('references.id'))
    reference: Mapped[Reference] = relationship(back_populates='meanings')
