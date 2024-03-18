from typing import Annotated, Optional

from pydantic import BaseModel, Field
from pydantic.networks import AnyHttpUrl, UrlConstraints

from .base import Base


class Reference(Base):
    reference: str
    url: str | None


class ReferenceExport(Reference):
    pass


class ReferencePublic(Reference):
    pass


class ReferenceCreate(BaseModel):
    reference: str = Field(min_length=3, max_length=280)
    url: Optional[
        Annotated[
            AnyHttpUrl,
            UrlConstraints(max_length=2048, allowed_schemes=['http', 'https']),
        ]
    ]


class ReferenceUpdate(ReferenceCreate):
    pass
