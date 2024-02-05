from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from .word import Word
else:
    Word = "Word"

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, PermissionType


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(15))
    last_name: Mapped[str] = mapped_column(String(15))
    name: Mapped[str] = mapped_column(String(31))
    email: Mapped[str] = mapped_column(String(319), unique=True)
    password: Mapped[str] = mapped_column(String(128))  # TODO: definir tamanho baseado na encriptação
    permission: Mapped[Optional[PermissionType]] = mapped_column(default=PermissionType.GUEST)

    words: Mapped[List[Word]] = relationship(back_populates="word", cascade="delete, all")
