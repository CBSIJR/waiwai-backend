from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user import User
    from .word import Word
else:
    User = 'User'
    Word = 'Word'

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func

from .base import Base, WordStatus


class WordReview(Base):
    """
    Registra cada decisão de revisão de um ADMIN sobre uma palavra.

    Cada instância representa um evento imutável no histórico de moderação,
    permitindo auditoria completa do fluxo de aprovação.
    """

    __tablename__ = 'word_reviews'

    id: Mapped[int] = mapped_column(primary_key=True)

    word_id: Mapped[int] = mapped_column(ForeignKey('words.id', ondelete='CASCADE'))
    reviewer_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))

    status: Mapped[WordStatus]
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    word: Mapped[Word] = relationship(back_populates='reviews')
    reviewer: Mapped[User] = relationship()
