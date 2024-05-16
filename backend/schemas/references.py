from typing import Annotated, Optional

from pydantic import BaseModel, Field
from pydantic.networks import AnyHttpUrl, UrlConstraints

from .base import Base


class Reference(Base):
    reference: str
    year: int
    authors: str
    url: str | None


class ReferenceExport(Reference):
    pass


class ReferencePublic(Reference):
    pass


class ReferenceCreate(BaseModel):
    reference: str = Field(min_length=3, max_length=350)
    year: Optional[int] = Field(min_length=1900, max_length=9999)
    authors: str = Field(min_length=3, max_length=350)
    url: Optional[
        Annotated[
            AnyHttpUrl,
            UrlConstraints(max_length=2048, allowed_schemes=['http', 'https']),
        ]
    ]


class ReferenceUpdate(ReferenceCreate):
    pass
