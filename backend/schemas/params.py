from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


# https://github.com/tiangolo/fastapi/discussions/10454#discussioncomment-7316522
class Params(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = Field(Query(default=100, ge=1, le=500))


class ParamsCategory(Params):
    q: Optional[str] = Query('')


class ParamsReference(Params):
    q: Optional[str] = Query(None, min_length=1, max_length=50)


class ParamsMeaning(Params):
    q: Optional[str] = Query(None, min_length=1, max_length=50)


class ParamsWordMeaning(ParamsMeaning):
    pass


class ParamsAttachments(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = Field(Query(default=5, ge=1, le=500))

