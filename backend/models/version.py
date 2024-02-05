from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Version(Base):
    __tablename__ = 'version'

    id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[float] = mapped_column(NUMERIC)

    words: Mapped[int]
    meanings: Mapped[int]
    categories: Mapped[int]
    references: Mapped[int]
    attachments: Mapped[int]
