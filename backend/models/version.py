from datetime import datetime

from sqlalchemy.dialects.postgresql import NUMERIC, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Version(Base):
    __tablename__ = 'version'

    id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[float] = mapped_column(NUMERIC)

    words: Mapped[datetime] = mapped_column(TIMESTAMP)
    meanings: Mapped[datetime] = mapped_column(TIMESTAMP)
    categories: Mapped[datetime] = mapped_column(TIMESTAMP)
    references: Mapped[datetime] = mapped_column(TIMESTAMP)
    attachments: Mapped[datetime] = mapped_column(TIMESTAMP)
    users: Mapped[datetime] = mapped_column(TIMESTAMP)
