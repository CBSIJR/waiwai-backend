from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .attachment import Attachment
    from .word import Word
    from .meaning import Meaning
else:
    Word = 'Word'
    Category = 'Category'
    Attachment = 'Attachment'

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, PermissionType


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(15))
    last_name: Mapped[str] = mapped_column(String(15))
    full_name: Mapped[str] = mapped_column(String(31))
    email: Mapped[str] = mapped_column(String(319), unique=True)
    password: Mapped[str] = mapped_column(
        String(128)
    )  # TODO: definir tamanho baseado na encriptação
    permission: Mapped[Optional[PermissionType]] = mapped_column(
        default=PermissionType.GUEST
    )

    meanings: Mapped[Optional[List[Meaning]]] = relationship(
        back_populates='user', cascade='delete, all'
    )

    words: Mapped[Optional[List[Word]]] = relationship(
        back_populates='user', cascade='delete, all'
    )

    attachments: Mapped[Optional[List[Attachment]]] = relationship(
        back_populates='user', cascade='delete, all'
    )
