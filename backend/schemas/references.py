from typing import Annotated, Optional

from pydantic import BaseModel, Field, field_validator
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
    
    @field_validator('reference')
    def reference_validator(cls, v: str):
        # Remove espaços extras no início/fim
        v = v.strip()

        # Substitui múltiplos espaços por apenas um
        v = ' '.join(v.split())

        assert all(c.isalpha() or c.isspace() or c in {';',',', '.'} for c in v), 'Deve conter apenas letras, espaços ou ponto e vírgula, vírgula e ponto final.'
        return v.capitalize()
    
    @field_validator('authors')
    def authors_validator(cls, v: str):
        # Remove espaços extras no início/fim
        v = v.strip()

        # Substitui múltiplos espaços por apenas um
        v = ' '.join(v.split())

        assert all(c.isalpha() or c.isspace() or c in {';',',', '.'} for c in v), 'Deve conter apenas letras, espaços ou ponto e vírgula, vírgula e ponto final.'
        return v.capitalize()


class ReferenceUpdate(ReferenceCreate):
    pass
