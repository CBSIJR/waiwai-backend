from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .attachment import Attachment
    from .category import Category
    from .meaning import Meaning
    from .user import User
else:
    Category = 'Category'
    User = 'User'
    Attachment = 'Attachment'
    Meaning = 'Meaning'

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func

from .base import Base, WordCategory


class Word(Base):
    __tablename__ = 'words'

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(50), unique=True)
    # TODO: Dinamicamente desabilitar campos
    # phonemic: Mapped[Optional[str]] = mapped_column(String(120))
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(back_populates='words')

    attachments: Mapped[Optional[List[Attachment]]] = relationship(
        back_populates='word', cascade='delete, all'
    )

    meanings: Mapped[Optional[List[Meaning]]] = relationship(
        back_populates='word', cascade='delete, all'
    )

    categories: Mapped[Optional[List[Category]]] = relationship(
        secondary=WordCategory, back_populates='words'
    )
