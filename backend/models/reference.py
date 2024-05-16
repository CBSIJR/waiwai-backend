from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .meaning import Meaning
else:
    Meaning = 'Meaning'

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Reference(Base):
    __tablename__ = 'references'

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(350), unique=True)
    year: Mapped[Optional[int]] = mapped_column(Integer)
    authors: Mapped[str] = mapped_column(String(350))
    url: Mapped[Optional[str]] = mapped_column(String(2048))

    meanings: Mapped[Optional[List[Meaning]]] = relationship(
        back_populates='reference'
    )
