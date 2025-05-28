from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, JWTBearer, get_current_user
from backend.configs import get_async_session
from backend.repositories import Attachments
from backend.schemas import (
    AttachmentCreate,
    AttachmentData,
    AttachmentPublic,
    BaseResponse,
    BaseResponsePage,
    CreatedResponse,
    ParamsAttachments,
    PermissionType,
    UserAuth,
)

from .base import Local

local = Local()
security = JWTBearer()
router = APIRouter(
    prefix='/words/{word_id}/attachments',
    tags=['Palavras Anexos'],
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=BaseResponsePage[List[AttachmentPublic]],
)
async def list_meanings(
    word_id: int,
    params: ParamsAttachments = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    meanings = await Attachments(session).get_list_by_word_id(word_id, params)
    total = await Attachments(session).count()
    return BaseResponsePage[AttachmentPublic](data=meanings, total_items=total)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN, PermissionType.USER]),
    ],
    response_model=BaseResponse[CreatedResponse],
)
async def create_attachment(
    word_id: int,
    file: AttachmentData = Depends(local),
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    attach = AttachmentCreate(
        uuid=file.uuid,
        filename=file.filename,
        filedir=file.filedir,
        url=file.url,
        content_type=file.content_type,
        word_id=word_id,
        user_id=current_user.id,
    )

    result = await Attachments(session).create(attach)
    return BaseResponse[CreatedResponse](data=CreatedResponse(id=result.id))
