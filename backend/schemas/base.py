import enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing_extensions import Annotated, Doc

T = TypeVar('T')


class WordCategoryExport(BaseModel):
    word_id: int
    category_id: int


class PermissionType(str, enum.Enum):
    GUEST = 'GUEST'
    USER = 'USER'
    ADMIN = 'ADMIN'


class Message(BaseModel):
    detail: str


class Base(BaseModel):
    id: int
    model_config = {'from_attributes': True}


class CreatedResponse(Base):
    pass


class BaseResponse(BaseModel, Generic[T]):
    data: Union[T, List[T]]


class BaseResponsePage(BaseResponse):
    total_items: int


class ErrorResponseMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: ErrorResponseMessage
    model_config = {'from_attributes': True}


class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: Annotated[
            int,
            Doc(
                """
                HTTP status code to send to the client.
                """
            ),
        ],
        detail: Annotated[
            Any,
            Doc(
                """
                Any data to be sent to the client in the `detail` key of the JSON
                response.
                """
            ),
        ] = None,
        headers: Annotated[
            Optional[Dict[str, str]],
            Doc(
                """
                Any headers to send to the client in the response.
                """
            ),
        ] = None,
    ) -> None:
        super().__init__(
            status_code=status_code, detail=dict(msg=detail), headers=headers
        )
