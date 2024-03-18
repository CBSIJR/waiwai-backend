from pydantic import BaseModel, Field

from .base import Base


class Version(Base):
    version: float
    words: int
    meanings: int
    categories: int
    references: int
    attachments: int


class VersionPublic(BaseModel):
    version: float
    words: int
    meanings: int
    categories: int
    references: int
    attachments: int

