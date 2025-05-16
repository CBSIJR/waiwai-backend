from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .base import Base


class Attachment(Base):
    uuid: UUID
    filename: str
    filedir: str
    url: str
    content_type: str
    user_id: int
    word_id: int
    created_at: datetime
    updated_at: datetime


class AttachmentPublic(Attachment):
    pass


class AttachmentExport(Attachment):
    pass


class AttachmentData(BaseModel):
    uuid: UUID
    filename: str
    filedir: str
    url: str
    content_type: str


class AttachmentCreate(AttachmentData):
    user_id: int
    word_id: int


class AttachmentUpdate(AttachmentCreate):
    pass
