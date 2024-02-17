from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .word import Word
else:
    Word = 'Word'

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func

from .base import Base


class Attachment(Base):
    __tablename__ = 'attachments'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID]
    path: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    word_id: Mapped[int] = mapped_column(ForeignKey('words.id'))
    word: Mapped[Word] = relationship(back_populates='attachments')
