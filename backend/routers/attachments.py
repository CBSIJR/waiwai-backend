from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, JWTBearer
from backend.configs import get_async_session
from backend.repositories import Attachments
from backend.schemas import (
    AttachmentPublic,
    Message,
    PermissionType,
)

router = APIRouter(
    prefix='/attachments',
    tags=['Uploads'],
)
security = JWTBearer()


@router.get(
    '/{attachment_id}',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': Message}},
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
        Authorization([PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': Message},
        '404': {'model': Message},
        '409': {'model': Message},
    },
)
async def delete_meaning(
    attachment_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await Attachments(session).delete_by_id(attachment_id)
