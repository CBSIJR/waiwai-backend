import logging
import os

from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.configs import get_async_session
from backend.repositories import Attachments
from backend.schemas import CustomHTTPException
from backend.utils import get_logger

SAFE_DIRECTORY = os.path.abspath('backend/static')


router = APIRouter()


@router.get('/uploads/{attachment_id}')
async def get_static_file(
    attachment_id: int,
    session: AsyncSession = Depends(get_async_session),
    log: logging.Logger = Depends(get_logger),
):
    attachment = await Attachments(session).get_by_id(attachment_id)
    filename = attachment.url.removeprefix('/uploads/')
    requested_path = os.path.abspath(os.path.join(SAFE_DIRECTORY, filename))
    log.info(f'Requested path: {requested_path}')
    log.info(f'Attachment path: {attachment.url}')
    log.info(f'SAFE_DIRECTORY: {SAFE_DIRECTORY}')
    if not requested_path.startswith(SAFE_DIRECTORY):
        raise CustomHTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Acesso negado.'
        )

    if not os.path.isfile(requested_path):
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Arquivo não encontrado.',
        )

    return FileResponse(
        requested_path,
        media_type=attachment.content_type,
        headers={'Cross-Origin-Resource-Policy': 'cross-origin'},
    )
