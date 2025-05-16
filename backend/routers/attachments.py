from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, JWTBearer, get_current_user
from backend.configs import get_async_session
from backend.repositories import Attachments
from backend.schemas import (
    AttachmentExport,
    AttachmentPublic,
    ErrorResponse,
    PermissionType,
    UserAuth,
)

router = APIRouter(
    prefix='/attachments',
    tags=['Anexos'],
)
security = JWTBearer()


@router.get(
    '/{attachment_id}',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': ErrorResponse}},
    response_model=AttachmentPublic,
)
async def get_meaning(
    attachment_id: int, session: AsyncSession = Depends(get_async_session)
):
    attachment = await Attachments(session).get_by_id(attachment_id)
    return attachment


@router.delete(
    '/{attachment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.USER, PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
    },
)
async def delete_meaning(
    attachment_id: int,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await Attachments(session).delete_by_id(attachment_id, current_user)


@router.get(
    '/export/all',
    status_code=status.HTTP_200_OK,
    response_model=List[AttachmentExport],
)
async def get_export(session: AsyncSession = Depends(get_async_session)):
    attachments = await Attachments(session).all()
    return attachments
