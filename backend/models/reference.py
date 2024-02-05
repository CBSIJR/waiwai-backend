from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from .meaning import Meaning
else:
    Meaning = "Meaning"

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base


class Reference(Base):
    __tablename__ = 'references'

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(80), unique=True)
    url: Mapped[str] = mapped_column(String(2048), unique=True)

    meanings: Mapped[Optional[List[Meaning]]] = relationship(back_populates="reference")
