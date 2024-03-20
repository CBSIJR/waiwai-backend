from datetime import datetime

from pydantic import BaseModel

from .base import Base


class Version(Base):
    version: float
    words: datetime
    meanings: datetime
    categories: datetime
    references: datetime
    attachments: datetime
    users: datetime


class VersionPublic(BaseModel):
    version: float
    words: datetime
    meanings: datetime
    categories: datetime
    references: datetime
    attachments: datetime
    users: datetime
