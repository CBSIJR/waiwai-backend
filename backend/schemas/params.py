from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
import unicodedata
from backend.models.base import WordStatus

class ParamsQuery(BaseModel):
    q: Optional[str] = Query(None, min_length=1, max_length=50)


# https://github.com/tiangolo/fastapi/discussions/10454#discussioncomment-7316522


class Params(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = Field(Query(default=100, ge=1, le=500))


class ParamsCategory(Params):
    q: Optional[str] = Query('')


class ParamsPageQuery(Params, ParamsQuery):
    pass

class ParamsWordQuery(ParamsPageQuery):
    starts_with: Optional[str] = Query(None, min_length=1, max_length=1)
    status: Optional[WordStatus] = Query(None)
    
    @field_validator("starts_with")
    def format_starts_with(cls, v):
        if v:
            return unicodedata.normalize("NFD", v).encode("ascii", "ignore").decode("utf-8")
        
class ParamsReference(Params):
    q: Optional[str] = Query(None, min_length=1, max_length=50)


class ParamsMeaning(Params):
    q: Optional[str] = Query(None, min_length=1, max_length=50)


class ParamsWordMeaning(ParamsMeaning):
    pass


class ParamsAttachments(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = Field(Query(default=5, ge=1, le=500))
