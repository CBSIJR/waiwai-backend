from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .meaning import Meaning
else:
    Meaning = 'Meaning'

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Reference(Base):
    __tablename__ = 'references'

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(280), unique=True)
    url: Mapped[Optional[str]] = mapped_column(String(2048))

    meanings: Mapped[Optional[List[Meaning]]] = relationship(
        back_populates='reference'
    )
