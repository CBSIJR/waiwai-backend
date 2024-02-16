from pydantic import BaseModel, Field
from fastapi import Query


# https://github.com/tiangolo/fastapi/discussions/10454#discussioncomment-7316522
class Params(BaseModel):
    page: int = 1
    page_size: int | None = Field(Query(default=100, ge=1, le=500))
