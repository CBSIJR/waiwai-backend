from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
if TYPE_CHECKING:
    from .user import User
    from .attachment import Attachment
    from .meaning import Meaning
    from .category import Category
else:
    Category = "Category"
    User = "User"
    Attachment = "Attachment"
    Meaning = "Meaning"

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func

from .base import Base, WordCategory

from datetime import datetime


class Word(Base):
    __tablename__ = 'words'

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          onupdate=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="words")

    attachments: Mapped[Optional[List[Attachment]]] = relationship(back_populates="word", cascade="delete, all")

    meanings: Mapped[Optional[List[Meaning]]] = relationship(back_populates="word", cascade="delete, all")

    categories: Mapped[Optional[List[Category]]] = relationship(
        secondary=WordCategory, back_populates="words"
    )
